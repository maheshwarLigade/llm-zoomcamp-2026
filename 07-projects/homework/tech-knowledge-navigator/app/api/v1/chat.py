"""
Chat API

Main RAG endpoint.

Responsibilities
----------------
* Validate request
* Invoke RAG pipeline
* Return formatted response

The endpoint itself should NOT contain any retrieval
or LLM logic.

Author
------
Tech Knowledge Navigator
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from pydantic import BaseModel
from pydantic import Field

from app.services.chat_service import ChatService
from app.api.deps import get_chat_service

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


###########################################################################
# Request Models
###########################################################################


class ChatRequest(BaseModel):
    """
    Chat request payload.
    """

    query: str = Field(
        ...,
        min_length=3,
        max_length=5000,
        description="Natural language user query.",
    )

    session_id: Optional[UUID] = Field(
        default=None,
        description="Conversation session identifier.",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of retrieved documents.",
    )

    temperature: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0,
    )

    use_hybrid_search: bool = Field(
        default=True,
        description="Use hybrid retrieval.",
    )

    use_reranker: bool = Field(
        default=True,
        description="Enable cross encoder reranker.",
    )

    rewrite_query: bool = Field(
        default=True,
        description="Rewrite user query before retrieval.",
    )


###########################################################################
# Response Models
###########################################################################


class SourceDocument(BaseModel):
    """
    Retrieved source document.
    """

    document_id: str

    title: str

    score: float

    source: str

    chunk: str


class ChatResponse(BaseModel):
    """
    Chat response.
    """

    answer: str

    session_id: UUID

    model: str

    latency_ms: int

    rewritten_query: Optional[str]

    retrieved_documents: int

    sources: list[SourceDocument]


###########################################################################
# Endpoint
###########################################################################


@router.post(
    "",
    response_model=ChatResponse,
    summary="Ask a question",
    description="Primary Retrieval-Augmented Generation endpoint.",
)
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    """
    Executes complete RAG pipeline.

    Flow

    User Query

        ↓

    Query Rewrite

        ↓

    Hybrid Retrieval

        ↓

    Re-ranking

        ↓

    Prompt Builder

        ↓

    LLM

        ↓

    Response
    """

    try:

        response = await chat_service.chat(request)

        return response

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {exc}",
        )