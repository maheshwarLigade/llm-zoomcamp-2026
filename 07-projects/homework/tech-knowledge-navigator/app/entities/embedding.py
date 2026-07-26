"""
Embedding Domain Entity

Represents vector embedding information
generated from document chunks.

Responsibilities:
- Track embedding lifecycle
- Store vector metadata
- Maintain model information
- Support vector database integration
- Enable embedding version management

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


from dataclasses import dataclass, field

from datetime import datetime, timezone

from enum import Enum

from typing import Any



###############################################################################
# Embedding Status
###############################################################################


class EmbeddingStatus(str, Enum):
    """
    Embedding processing lifecycle.
    """

    CREATED = "created"

    GENERATING = "generating"

    COMPLETED = "completed"

    FAILED = "failed"

    DELETED = "deleted"



###############################################################################
# Embedding Provider
###############################################################################


class EmbeddingProvider(str, Enum):
    """
    Supported embedding providers.
    """

    OPENAI = "openai"

    HUGGINGFACE = "huggingface"

    COHERE = "cohere"

    OLLAMA = "ollama"

    CUSTOM = "custom"



###############################################################################
# Embedding Entity
###############################################################################


@dataclass
class Embedding:
    """
    Embedding aggregate entity.

    Represents vector representation
    of a document chunk.

    Example:

        Chunk

          |
          |
       Embedding

          |
          |
    Vector Database Record

    """


    ###########################################################################
    # Identity
    ###########################################################################

    id: str


    chunk_id: str



    ###########################################################################
    # Model Information
    ###########################################################################

    model_name: str


    provider: EmbeddingProvider



    model_version: str | None = None



    ###########################################################################
    # Vector Information
    ###########################################################################

    dimension: int = 0


    vector: list[float] | None = None



    ###########################################################################
    # Storage Information
    ###########################################################################

    vector_store_id: str | None = None


    collection_name: str | None = None



    ###########################################################################
    # Processing State
    ###########################################################################

    status: EmbeddingStatus = (
        EmbeddingStatus.CREATED
    )


    error_message: str | None = None



    ###########################################################################
    # Similarity Search Metadata
    ###########################################################################

    metadata: dict[str, Any] = field(
        default_factory=dict
    )



    ###########################################################################
    # Versioning
    ###########################################################################

    embedding_version: int = 1



    ###########################################################################
    # Audit
    ###########################################################################

    created_at: datetime = field(
        default_factory=lambda:
        datetime.now(
            timezone.utc
        )
    )


    updated_at: datetime = field(
        default_factory=lambda:
        datetime.now(
            timezone.utc
        )
    )



    ###########################################################################
    # Lifecycle Methods
    ###########################################################################


    def start_generation(
        self,
    ):
        """
        Mark embedding generation started.
        """

        self.status = (
            EmbeddingStatus.GENERATING
        )

        self.updated_at = datetime.now(
            timezone.utc
        )



    def complete_generation(
        self,
        vector: list[float],
    ):
        """
        Store generated vector.
        """

        self.vector = vector

        self.dimension = len(
            vector
        )

        self.status = (
            EmbeddingStatus.COMPLETED
        )

        self.error_message = None

        self.updated_at = datetime.now(
            timezone.utc
        )



    def mark_failed(
        self,
        error: str,
    ):
        """
        Mark embedding generation failed.
        """

        self.status = (
            EmbeddingStatus.FAILED
        )

        self.error_message = error

        self.updated_at = datetime.now(
            timezone.utc
        )



    def delete(
        self,
    ):
        """
        Mark embedding deleted.
        """

        self.status = (
            EmbeddingStatus.DELETED
        )

        self.vector = None

        self.updated_at = datetime.now(
            timezone.utc
        )



    ###########################################################################
    # Vector Store Management
    ###########################################################################


    def attach_vector_store(
        self,
        vector_store_id: str,
        collection_name: str,
    ):
        """
        Attach vector database reference.
        """

        self.vector_store_id = (
            vector_store_id
        )

        self.collection_name = (
            collection_name
        )

        self.updated_at = datetime.now(
            timezone.utc
        )



    ###########################################################################
    # Metadata Management
    ###########################################################################


    def update_metadata(
        self,
        values: dict[str, Any],
    ):
        """
        Update embedding metadata.
        """

        self.metadata.update(
            values
        )



    ###########################################################################
    # Version Management
    ###########################################################################


    def create_new_version(
        self,
    ):
        """
        Increment embedding version.

        Used when:
        - embedding model changes
        - chunk content changes
        """

        self.embedding_version += 1

        self.updated_at = datetime.now(
            timezone.utc
        )



    ###########################################################################
    # Validation
    ###########################################################################


    def is_ready(
        self,
    ) -> bool:
        """
        Check if embedding can participate
        in similarity search.
        """

        return (

            self.status
            ==
            EmbeddingStatus.COMPLETED

            and

            self.vector is not None

        )



    def similarity_metadata(
        self,
    ) -> dict[str, Any]:
        """
        Metadata stored with vector.

        Used by:
        - Qdrant
        - Pinecone
        - Chroma
        - pgvector
        """

        return {

            "embedding_id":
                self.id,

            "chunk_id":
                self.chunk_id,

            "model":
                self.model_name,

            "provider":
                self.provider.value,

            "version":
                self.embedding_version,

        }



    ###########################################################################
    # Serialization
    ###########################################################################


    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Convert entity to dictionary.
        """

        return {

            "id":
                self.id,

            "chunk_id":
                self.chunk_id,

            "model":
                self.model_name,

            "provider":
                self.provider.value,

            "dimension":
                self.dimension,

            "status":
                self.status.value,

            "vector_store_id":
                self.vector_store_id,

            "created_at":
                self.created_at.isoformat(),

            "updated_at":
                self.updated_at.isoformat(),

        }