"""
Embedding Repository Interface

Defines persistence contract for Embedding entity.

Responsibilities:
- Store embedding metadata
- Manage vector references
- Track embedding lifecycle
- Support retrieval pipeline
- Enable re-indexing workflows

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


from abc import ABC, abstractmethod


from typing import Optional


from app.entities.embedding import (
    Embedding,
    EmbeddingStatus,
)



###############################################################################
# Embedding Repository Interface
###############################################################################


class EmbeddingRepository(
    ABC
):
    """
    Repository contract for Embedding aggregate.

    Embedding lifecycle:

        Chunk

          |

          v

     Generate Vector

          |

          v

      Embedding

          |

          v

     Vector Database


    """



    ###########################################################################
    # Create / Update
    ###########################################################################


    @abstractmethod
    async def save(
        self,
        embedding: Embedding,
    ) -> Embedding:
        """
        Save embedding.

        Creates new embedding or updates
        existing record.
        """

        raise NotImplementedError



    @abstractmethod
    async def save_many(
        self,
        embeddings: list[Embedding],
    ) -> list[Embedding]:
        """
        Bulk save embeddings.

        Used during batch ingestion.

        Example:

        1000 chunks
             |
             |
        Generate embeddings
             |
             |
        save_many()

        """

        raise NotImplementedError



    @abstractmethod
    async def update(
        self,
        embedding: Embedding,
    ) -> Embedding:
        """
        Update embedding metadata.
        """

        raise NotImplementedError



    ###########################################################################
    # Retrieval Operations
    ###########################################################################


    @abstractmethod
    async def find_by_id(
        self,
        embedding_id: str,
    ) -> Optional[Embedding]:
        """
        Find embedding by id.
        """

        raise NotImplementedError



    @abstractmethod
    async def find_by_chunk_id(
        self,
        chunk_id: str,
    ) -> Optional[Embedding]:
        """
        Find embedding associated with chunk.
        """

        raise NotImplementedError



    @abstractmethod
    async def find_by_chunk_ids(
        self,
        chunk_ids: list[str],
    ) -> list[Embedding]:
        """
        Retrieve embeddings for multiple chunks.
        """

        raise NotImplementedError



    ###########################################################################
    # Document Level Operations
    ###########################################################################


    @abstractmethod
    async def find_by_document_id(
        self,
        document_id: str,
    ) -> list[Embedding]:
        """
        Retrieve embeddings belonging
        to a document.

        Used for:

        - document deletion
        - re-indexing
        - migration

        """

        raise NotImplementedError



    ###########################################################################
    # Status Management
    ###########################################################################


    @abstractmethod
    async def update_status(
        self,
        embedding_id: str,
        status: EmbeddingStatus,
        error_message: str | None = None,
    ) -> None:
        """
        Update embedding generation status.

        Example:

        CREATED
           |
           v
        GENERATING
           |
           v
        COMPLETED

        """

        raise NotImplementedError



    ###########################################################################
    # Vector Store Integration
    ###########################################################################


    @abstractmethod
    async def attach_vector_reference(
        self,
        embedding_id: str,
        vector_store_id: str,
        collection_name: str,
    ) -> None:
        """
        Attach vector database reference.

        Example:

        Qdrant point id
        Pinecone vector id

        """

        raise NotImplementedError



    @abstractmethod
    async def remove_vector_reference(
        self,
        embedding_id: str,
    ) -> None:
        """
        Remove vector store mapping.
        """

        raise NotImplementedError



    ###########################################################################
    # Search Support
    ###########################################################################


    @abstractmethod
    async def find_ready_embeddings(
        self,
        limit: int = 100,
    ) -> list[Embedding]:
        """
        Find embeddings ready for retrieval.

        Conditions:

        status = COMPLETED
        vector exists

        """

        raise NotImplementedError



    @abstractmethod
    async def find_missing_embeddings(
        self,
        limit: int = 100,
    ) -> list[Embedding]:
        """
        Find chunks requiring embedding generation.

        Used by:

        background workers

        """

        raise NotImplementedError



    ###########################################################################
    # Model Management
    ###########################################################################


    @abstractmethod
    async def find_by_model(
        self,
        model_name: str,
    ) -> list[Embedding]:
        """
        Find embeddings created by model.

        Useful for:

        - migration
        - comparison
        - cleanup

        """

        raise NotImplementedError



    @abstractmethod
    async def find_outdated_embeddings(
        self,
        model_name: str,
        model_version: str | None = None,
    ) -> list[Embedding]:
        """
        Find embeddings requiring regeneration.

        Example:

        Old:
          text-embedding-ada

        New:
          text-embedding-3-small

        """

        raise NotImplementedError



    ###########################################################################
    # Delete Operations
    ###########################################################################


    @abstractmethod
    async def delete(
        self,
        embedding_id: str,
    ) -> bool:
        """
        Delete embedding.

        Returns:

        True:
            deleted

        False:
            not found

        """

        raise NotImplementedError



    @abstractmethod
    async def delete_by_chunk_id(
        self,
        chunk_id: str,
    ) -> bool:
        """
        Delete embedding by chunk.
        """

        raise NotImplementedError



    ###########################################################################
    # Statistics
    ###########################################################################


    @abstractmethod
    async def count(
        self,
    ) -> int:
        """
        Total embeddings count.
        """

        raise NotImplementedError



    @abstractmethod
    async def count_by_status(
        self,
        status: EmbeddingStatus,
    ) -> int:
        """
        Count embeddings by status.
        """

        raise NotImplementedError



###############################################################################
# Embedding Search Criteria
###############################################################################


class EmbeddingSearchCriteria:
    """
    Dynamic embedding search criteria.

    Example:

    {
        "model": "text-embedding-3-small",
        "status": "completed"
    }

    """



    def __init__(
        self,
        model_name: str | None = None,
        provider: str | None = None,
        status: EmbeddingStatus | None = None,
        limit: int = 10,
    ):

        self.model_name = model_name

        self.provider = provider

        self.status = status

        self.limit = limit



###############################################################################
# Embedding Migration Specification
###############################################################################


class EmbeddingMigrationCriteria:
    """
    Defines embedding migration criteria.

    Used when changing embedding models.

    Example:

        Existing:
            OpenAI ada-002

        Target:
            text-embedding-3-small

    """



    def __init__(
        self,
        source_model: str,
        target_model: str,
    ):

        self.source_model = source_model

        self.target_model = target_model