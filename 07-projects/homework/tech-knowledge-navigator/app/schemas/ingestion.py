"""
Ingestion API Schemas

Pydantic models used for document ingestion,
pipeline execution, and ingestion monitoring.

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
# Enums
###############################################################################


class IngestionStatus(str, Enum):
    """
    Ingestion job status.
    """

    CREATED = "created"

    QUEUED = "queued"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"



class DocumentType(str, Enum):
    """
    Supported document formats.
    """

    PDF = "pdf"

    TEXT = "text"

    MARKDOWN = "markdown"

    HTML = "html"

    JSON = "json"

    CSV = "csv"

    WEB_PAGE = "web_page"

    YOUTUBE_TRANSCRIPT = "youtube_transcript"



class ChunkingStrategy(str, Enum):
    """
    Text chunking strategies.
    """

    FIXED_SIZE = "fixed_size"

    RECURSIVE = "recursive"

    SEMANTIC = "semantic"



###############################################################################
# Ingestion Request
###############################################################################


class IngestionRequest(BaseModel):
    """
    Start ingestion pipeline.

    Example:
        Upload documents
        Crawl website
        Import dataset
    """

    dataset_name: str = Field(
        ...,
        examples=[
            "wikipedia-ai-subset",
            "youtube-transcripts",
        ],
    )

    source_path: str

    document_type: DocumentType

    chunking_strategy: ChunkingStrategy = (
        ChunkingStrategy.RECURSIVE
    )

    chunk_size: int = Field(
        default=512,
        ge=100,
        le=2000,
    )

    chunk_overlap: int = Field(
        default=50,
        ge=0,
        le=500,
    )

    generate_embeddings: bool = True

    index_vector_store: bool = True

    index_text_search: bool = True

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )



###############################################################################
# Ingestion Configuration
###############################################################################


class EmbeddingConfiguration(BaseModel):
    """
    Embedding model configuration.
    """

    provider: str

    model_name: str

    dimension: int



class VectorStoreConfiguration(BaseModel):
    """
    Vector database configuration.
    """

    provider: str = "qdrant"

    collection_name: str

    distance_metric: str = "cosine"



class SearchIndexConfiguration(BaseModel):
    """
    Text search configuration.
    """

    provider: str = "opensearch"

    index_name: str



class IngestionConfiguration(BaseModel):
    """
    Complete pipeline configuration.
    """

    embedding: EmbeddingConfiguration

    vector_store: VectorStoreConfiguration

    search_index: SearchIndexConfiguration



###############################################################################
# Ingestion Response
###############################################################################


class IngestionResponse(BaseModel):
    """
    Response after ingestion creation.
    """

    ingestion_id: UUID = Field(
        default_factory=uuid4,
    )

    dataset_name: str

    status: IngestionStatus

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )

    message: str



###############################################################################
# Ingestion Progress
###############################################################################


class IngestionProgress(BaseModel):
    """
    Runtime ingestion progress.
    """

    ingestion_id: UUID

    status: IngestionStatus

    total_documents: int = 0

    processed_documents: int = 0

    total_chunks: int = 0

    embedded_chunks: int = 0

    indexed_chunks: int = 0

    progress_percentage: float = Field(
        default=0.0,
        ge=0,
        le=100,
    )

    current_step: str | None = None

    error_message: str | None = None



###############################################################################
# Ingestion Result
###############################################################################


class IngestionResult(BaseModel):
    """
    Final ingestion pipeline result.
    """

    ingestion_id: UUID

    status: IngestionStatus

    documents_processed: int

    chunks_created: int

    embeddings_generated: int

    vectors_indexed: int

    text_documents_indexed: int

    execution_time_seconds: float

    warnings: list[str] = Field(
        default_factory=list,
    )



###############################################################################
# Ingestion History
###############################################################################


class IngestionHistoryItem(BaseModel):
    """
    Historical ingestion execution.
    """

    ingestion_id: UUID

    dataset_name: str

    status: IngestionStatus

    documents_processed: int

    started_at: datetime | None

    completed_at: datetime | None



class IngestionHistoryResponse(BaseModel):
    """
    Paginated ingestion history.
    """

    items: list[IngestionHistoryItem]

    total: int

    page: int

    page_size: int



###############################################################################
# Retry Failed Ingestion
###############################################################################


class RetryIngestionRequest(BaseModel):
    """
    Retry failed ingestion.
    """

    ingestion_id: UUID

    restart_from_step: str | None = None



###############################################################################
# Pipeline Health
###############################################################################


class IngestionPipelineHealth(BaseModel):
    """
    Pipeline component health.

    Used by monitoring dashboard.
    """

    scheduler_status: str

    worker_status: str

    queue_size: int

    running_jobs: int

    failed_jobs: int



###############################################################################
# API Response Wrapper
###############################################################################


class IngestionApiResponse(BaseModel):
    """
    Standard API wrapper.
    """

    success: bool = True

    data: IngestionResponse

    request_id: str

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
    )

    model_config = ConfigDict(
        from_attributes=True,
    )