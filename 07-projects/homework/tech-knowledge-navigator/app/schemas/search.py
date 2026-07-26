"""
Search API Schemas

Pydantic models for:
- Semantic search
- Keyword search
- Hybrid search
- Query rewriting
- Document reranking
- Retrieval results

Author
------
Tech Knowledge Navigator
"""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


###############################################################################
# Search Enums
###############################################################################


class SearchType(str, Enum):
    """
    Search strategy.
    """

    VECTOR = "vector"

    KEYWORD = "keyword"

    HYBRID = "hybrid"



class RankingMethod(str, Enum):
    """
    Document ranking strategy.
    """

    NONE = "none"

    CROSS_ENCODER = "cross_encoder"

    LLM_RERANKER = "llm_reranker"



class DistanceMetric(str, Enum):
    """
    Vector similarity metric.
    """

    COSINE = "cosine"

    DOT_PRODUCT = "dot_product"

    EUCLIDEAN = "euclidean"



###############################################################################
# Search Request
###############################################################################


class SearchRequest(BaseModel):
    """
    Search request.

    Used for:
    - semantic search
    - keyword search
    - hybrid search
    """

    query: str = Field(
        ...,
        min_length=2,
        max_length=4000,
    )

    search_type: SearchType = (
        SearchType.HYBRID
    )

    top_k: int = Field(
        default=10,
        ge=1,
        le=100,
    )

    filters: dict[str, Any] = Field(
        default_factory=dict,
    )

    include_content: bool = True

    include_metadata: bool = True



###############################################################################
# Query Rewrite
###############################################################################


class QueryRewriteRequest(BaseModel):
    """
    Query rewriting request.

    Example:

    Original:
        "How does it work?"

    Rewritten:
        "How does hybrid search work in RAG?"
    """

    query: str

    conversation_history: list[str] = Field(
        default_factory=list,
    )

    enable_rewrite: bool = True



class QueryRewriteResponse(BaseModel):
    """
    Query rewrite response.
    """

    original_query: str

    rewritten_query: str

    confidence: float = Field(
        ge=0,
        le=1,
    )

    model: str



###############################################################################
# Vector Search
###############################################################################


class VectorSearchRequest(BaseModel):
    """
    Vector similarity search request.
    """

    query: str

    embedding_model: str

    top_k: int = Field(
        default=10,
        ge=1,
        le=100,
    )

    distance_metric: DistanceMetric = (
        DistanceMetric.COSINE
    )



###############################################################################
# Keyword Search
###############################################################################


class KeywordSearchRequest(BaseModel):
    """
    BM25 search request.
    """

    query: str

    index_name: str

    top_k: int = Field(
        default=10,
        ge=1,
        le=100,
    )

    minimum_score: float = 0.0



###############################################################################
# Hybrid Search Configuration
###############################################################################


class HybridSearchConfiguration(BaseModel):
    """
    Hybrid search tuning parameters.

    Combines:

    BM25 + Vector similarity
    """

    vector_weight: float = Field(
        default=0.5,
        ge=0,
        le=1,
    )

    keyword_weight: float = Field(
        default=0.5,
        ge=0,
        le=1,
    )

    fusion_algorithm: str = "rrf"



###############################################################################
# Reranking
###############################################################################


class RerankRequest(BaseModel):
    """
    Document reranking request.
    """

    query: str

    documents: list[str]

    ranking_method: RankingMethod = (
        RankingMethod.CROSS_ENCODER
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=50,
    )



class RerankedDocument(BaseModel):
    """
    Reranked document result.
    """

    document_id: str

    original_score: float

    rerank_score: float

    rank: int



###############################################################################
# Search Result
###############################################################################


class SearchDocument(BaseModel):
    """
    Retrieved document chunk.
    """

    document_id: str

    chunk_id: str

    title: str

    content: str | None = None

    score: float = Field(
        ge=0,
    )

    source: str | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )



###############################################################################
# Search Response
###############################################################################


class SearchResponse(BaseModel):
    """
    Search response.

    Returned after retrieval.
    """

    search_id: UUID = Field(
        default_factory=uuid4,
    )

    query: str

    rewritten_query: str | None = None

    search_type: SearchType

    results: list[SearchDocument]

    total_results: int

    execution_time_ms: float

    embedding_model: str | None = None

    reranking_applied: bool = False

    reranker_model: str | None = None

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )



###############################################################################
# Retrieval Evaluation Support
###############################################################################


class RetrievalExperimentRequest(BaseModel):
    """
    Compare retrieval approaches.

    Used for Zoomcamp retrieval evaluation.
    """

    dataset_name: str

    queries: list[str]

    approaches: list[SearchType]

    top_k: int = 10



class RetrievalExperimentResult(BaseModel):
    """
    Retrieval experiment result.
    """

    approach: SearchType

    precision: float

    recall: float

    mrr: float

    ndcg: float

    average_latency_ms: float



###############################################################################
# Search History
###############################################################################


class SearchHistoryItem(BaseModel):
    """
    Search history record.
    """

    search_id: UUID

    query: str

    search_type: SearchType

    result_count: int

    created_at: datetime



class SearchHistoryResponse(BaseModel):
    """
    Search history response.
    """

    items: list[SearchHistoryItem]

    total: int



###############################################################################
# Search API Wrapper
###############################################################################


class SearchApiResponse(BaseModel):
    """
    Standard API wrapper.
    """

    success: bool = True

    data: SearchResponse

    request_id: str

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
    )


    model_config = ConfigDict(
        from_attributes=True,
    )