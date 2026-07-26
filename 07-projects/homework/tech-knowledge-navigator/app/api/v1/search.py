"""
Search API

Provides retrieval-only endpoints for the knowledge base.

Responsibilities
----------------
* Keyword search (BM25)
* Vector search
* Hybrid search
* Similar document search
* Search suggestions

Business logic is delegated to SearchService.
"""

from enum import Enum
from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from pydantic import BaseModel
from pydantic import Field

from app.api.deps import get_search_service
from app.services.search_service import SearchService

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)

###############################################################################
# Enums
###############################################################################


class SearchType(str, Enum):
    KEYWORD = "keyword"
    VECTOR = "vector"
    HYBRID = "hybrid"


###############################################################################
# Request Models
###############################################################################


class SearchRequest(BaseModel):
    """
    Generic search request.
    """

    query: str = Field(
        ...,
        min_length=2,
        max_length=2000,
    )

    search_type: SearchType = SearchType.HYBRID

    top_k: int = Field(
        default=10,
        ge=1,
        le=50,
    )

    use_reranker: bool = True

    include_content: bool = True


###############################################################################
# Response Models
###############################################################################


class SearchResult(BaseModel):
    """
    Individual search result.
    """

    document_id: str

    chunk_id: str

    title: str

    source: str

    score: float

    content: Optional[str] = None

    metadata: dict = Field(default_factory=dict)


class SearchResponse(BaseModel):
    """
    Search response.
    """

    query: str

    search_type: SearchType

    total_results: int

    latency_ms: float

    results: List[SearchResult]


###############################################################################
# Generic Search
###############################################################################


@router.post(
    "",
    response_model=SearchResponse,
    summary="Search Knowledge Base",
)
async def search(
    request: SearchRequest,
    service: SearchService = Depends(get_search_service),
):
    """
    Executes the selected search strategy.
    """

    return await service.search(request)


###############################################################################
# Keyword Search
###############################################################################


@router.get(
    "/keyword",
    response_model=SearchResponse,
    summary="Keyword Search",
)
async def keyword_search(
    query: str = Query(..., min_length=2),
    top_k: int = Query(default=10, ge=1, le=50),
    service: SearchService = Depends(get_search_service),
):
    """
    Performs BM25 keyword search.
    """

    return await service.keyword_search(
        query=query,
        top_k=top_k,
    )


###############################################################################
# Vector Search
###############################################################################


@router.get(
    "/vector",
    response_model=SearchResponse,
    summary="Vector Search",
)
async def vector_search(
    query: str = Query(..., min_length=2),
    top_k: int = Query(default=10, ge=1, le=50),
    service: SearchService = Depends(get_search_service),
):
    """
    Performs semantic vector search.
    """

    return await service.vector_search(
        query=query,
        top_k=top_k,
    )


###############################################################################
# Hybrid Search
###############################################################################


@router.get(
    "/hybrid",
    response_model=SearchResponse,
    summary="Hybrid Search",
)
async def hybrid_search(
    query: str = Query(..., min_length=2),
    top_k: int = Query(default=10, ge=1, le=50),
    rerank: bool = True,
    service: SearchService = Depends(get_search_service),
):
    """
    Combines BM25 and vector search.
    """

    return await service.hybrid_search(
        query=query,
        top_k=top_k,
        rerank=rerank,
    )


###############################################################################
# Similar Documents
###############################################################################


@router.get(
    "/similar/{document_id}",
    response_model=SearchResponse,
    summary="Find Similar Documents",
)
async def similar_documents(
    document_id: str,
    top_k: int = Query(default=10, ge=1, le=50),
    service: SearchService = Depends(get_search_service),
):
    """
    Returns documents similar to the specified document.
    """

    return await service.similar_documents(
        document_id=document_id,
        top_k=top_k,
    )


###############################################################################
# Search Suggestions
###############################################################################


@router.get(
    "/suggest",
    response_model=List[str],
    summary="Search Suggestions",
)
async def search_suggestions(
    prefix: str = Query(..., min_length=1),
    limit: int = Query(default=10, ge=1, le=20),
    service: SearchService = Depends(get_search_service),
):
    """
    Returns query suggestions for autocomplete.
    """

    return await service.suggestions(
        prefix=prefix,
        limit=limit,
    )