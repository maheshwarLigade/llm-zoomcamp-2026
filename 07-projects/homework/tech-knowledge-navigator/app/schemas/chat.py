"""
Chat API Schemas

Pydantic models used by the Chat API.

Author
------
Tech Knowledge Navigator
"""

from datetime import datetime
from typing import Any
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


###############################################################################
# Source
###############################################################################


class SourceDocument(BaseModel):
    """
    Source document returned by retrieval.
    """

    document_id: str

    title: str

    chunk_id: str

    score: float = Field(..., ge=0.0, le=1.0)

    content: str

    metadata: dict[str, Any] = Field(default_factory=dict)

    url: str | None = None


###############################################################################
# Chat Message
###############################################################################


class ChatMessage(BaseModel):
    """
    Single chat message.
    """

    role: str = Field(
        ...,
        examples=["user", "assistant", "system"],
    )

    content: str

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
    )


###############################################################################
# Chat Request
###############################################################################


class ChatRequest(BaseModel):
    """
    Chat request.
    """

    conversation_id: UUID | None = None

    query: str = Field(
        ...,
        min_length=2,
        max_length=4000,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )

    use_hybrid_search: bool = True

    use_reranking: bool = True

    rewrite_query: bool = True

    stream: bool = False

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


###############################################################################
# Token Usage
###############################################################################


class TokenUsage(BaseModel):
    """
    Token usage statistics.
    """

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0


###############################################################################
# Retrieval Metadata
###############################################################################


class RetrievalMetadata(BaseModel):
    """
    Retrieval execution information.
    """

    query: str

    rewritten_query: str | None = None

    retrieval_time_ms: float

    reranking_time_ms: float | None = None

    total_documents: int

    search_strategy: str

    embedding_model: str

    reranker_model: str | None = None


###############################################################################
# Chat Response
###############################################################################


class ChatResponse(BaseModel):
    """
    Chat response.
    """

    conversation_id: UUID

    message_id: UUID = Field(
        default_factory=uuid4,
    )

    answer: str

    sources: list[SourceDocument] = Field(
        default_factory=list,
    )

    retrieval: RetrievalMetadata

    token_usage: TokenUsage

    model: str

    latency_ms: float

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )

    feedback_id: UUID | None = None


###############################################################################
# Streaming Chunk
###############################################################################


class ChatStreamChunk(BaseModel):
    """
    Streaming response chunk.
    """

    conversation_id: UUID

    chunk: str

    finished: bool = False


###############################################################################
# Chat History
###############################################################################


class ChatHistoryItem(BaseModel):
    """
    Chat history item.
    """

    message_id: UUID

    role: str

    content: str

    created_at: datetime


class ChatHistoryResponse(BaseModel):
    """
    Conversation history.
    """

    conversation_id: UUID

    messages: list[ChatHistoryItem]


###############################################################################
# Chat Feedback
###############################################################################


class ChatFeedbackRequest(BaseModel):
    """
    Feedback for a generated answer.
    """

    message_id: UUID

    rating: int = Field(
        ...,
        ge=1,
        le=5,
    )

    comment: str | None = Field(
        default=None,
        max_length=1000,
    )


###############################################################################
# Evaluation Result
###############################################################################


class ChatEvaluation(BaseModel):
    """
    Optional evaluation metrics.
    """

    faithfulness: float | None = None

    answer_relevancy: float | None = None

    context_precision: float | None = None

    context_recall: float | None = None


###############################################################################
# Generic API Response
###############################################################################


class ChatApiResponse(BaseModel):
    """
    Standard API response wrapper.
    """

    success: bool = True

    data: ChatResponse

    evaluation: ChatEvaluation | None = None

    request_id: str

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
    )

    model_config = ConfigDict(
        from_attributes=True,
    )