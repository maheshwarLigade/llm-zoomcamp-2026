"""
Chunk Repository Interface

Defines persistence contract for Chunk entity.

Chunks are the searchable units created
during document ingestion.

Responsibilities:
- Persist chunks
- Retrieve chunks
- Search chunks
- Manage chunk metadata
- Support retrieval pipeline

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


from abc import ABC, abstractmethod


from typing import Optional


from app.entities.chunk import Chunk



###############################################################################
# Chunk Repository Interface
###############################################################################


class ChunkRepository(
    ABC
):
    """
    Repository contract for Chunk aggregate.

    A chunk belongs to a document and is used by:

    - Vector search
    - Keyword search
    - Hybrid search
    - Reranking

    """



    ###########################################################################
    # Create / Update
    ###########################################################################


    @abstractmethod
    async def save(
        self,
        chunk: Chunk,
    ) -> Chunk:
        """
        Save a chunk.

        Creates new chunk or updates
        existing chunk.
        """

        raise NotImplementedError



    @abstractmethod
    async def save_many(
        self,
        chunks: list[Chunk],
    ) -> list[Chunk]:
        """
        Bulk save chunks.

        Used during ingestion.

        Example:

        Document
          |
          |
        Splitter
          |
          |
        100 chunks
          |
          |
        save_many()

        """

        raise NotImplementedError



    @abstractmethod
    async def update(
        self,
        chunk: Chunk,
    ) -> Chunk:
        """
        Update existing chunk.
        """

        raise NotImplementedError



    ###########################################################################
    # Read Operations
    ###########################################################################


    @abstractmethod
    async def find_by_id(
        self,
        chunk_id: str,
    ) -> Optional[Chunk]:
        """
        Find chunk by id.
        """

        raise NotImplementedError



    @abstractmethod
    async def find_by_document_id(
        self,
        document_id: str,
        limit: int = 100,
    ) -> list[Chunk]:
        """
        Retrieve all chunks belonging
        to a document.
        """

        raise NotImplementedError



    @abstractmethod
    async def find_by_ids(
        self,
        chunk_ids: list[str],
    ) -> list[Chunk]:
        """
        Retrieve chunks by multiple ids.

        Useful for:

        - Retrieval results
        - Reranking
        - Context building

        """

        raise NotImplementedError



    ###########################################################################
    # Search Operations
    ###########################################################################


    @abstractmethod
    async def search_by_keyword(
        self,
        keyword: str,
        limit: int = 10,
    ) -> list[Chunk]:
        """
        Keyword based search.

        Example:

        BM25 search

        """

        raise NotImplementedError



    @abstractmethod
    async def search_by_metadata(
        self,
        filters: dict,
        limit: int = 10,
    ) -> list[Chunk]:
        """
        Search chunks using metadata.

        Examples:

        {
            "document_type": "pdf",
            "author": "John"
        }

        """

        raise NotImplementedError



    ###########################################################################
    # Retrieval Support
    ###########################################################################


    @abstractmethod
    async def get_retrieval_candidates(
        self,
        document_ids: list[str] | None = None,
        limit: int = 100,
    ) -> list[Chunk]:
        """
        Retrieve candidate chunks.

        Used before:

        - Embedding search
        - Reranking
        - Context assembly

        """

        raise NotImplementedError



    ###########################################################################
    # Embedding Support
    ###########################################################################


    @abstractmethod
    async def find_without_embedding(
        self,
        limit: int = 100,
    ) -> list[Chunk]:
        """
        Find chunks that do not have embeddings.

        Used by ingestion workers.

        Flow:

        Chunk
          |
          |
        Generate Embedding
          |
          |
        Vector Store

        """

        raise NotImplementedError



    @abstractmethod
    async def attach_embedding(
        self,
        chunk_id: str,
        embedding_id: str,
    ) -> None:
        """
        Attach embedding reference
        to chunk.
        """

        raise NotImplementedError



    ###########################################################################
    # Delete Operations
    ###########################################################################


    @abstractmethod
    async def delete(
        self,
        chunk_id: str,
    ) -> bool:
        """
        Delete chunk.

        Returns:

        True:
            deleted

        False:
            not found

        """

        raise NotImplementedError



    @abstractmethod
    async def delete_by_document_id(
        self,
        document_id: str,
    ) -> int:
        """
        Delete all chunks
        belonging to document.

        Returns:

            number of deleted chunks

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
        Return total chunk count.
        """

        raise NotImplementedError



    @abstractmethod
    async def count_by_document(
        self,
        document_id: str,
    ) -> int:
        """
        Count chunks for document.
        """

        raise NotImplementedError



###############################################################################
# Chunk Specification
###############################################################################


class ChunkSpecification:
    """
    Dynamic filtering helper.

    Used for repository queries.

    Example:

    {
        "chunk_type": "text",
        "page_number": 10
    }

    """



    def __init__(
        self,
        filters: dict | None = None,
    ):

        self.filters = filters or {}



    def matches(
        self,
        chunk: Chunk,
    ) -> bool:
        """
        Check whether chunk matches filters.
        """

        for key, value in self.filters.items():

            if getattr(
                chunk,
                key,
                None,
            ) != value:

                return False


        return True



###############################################################################
# Retrieval Helper
###############################################################################


class ChunkSearchCriteria:
    """
    Search criteria object.

    Used by hybrid retrieval.

    Example:

    - keyword
    - metadata
    - document filter

    """



    def __init__(
        self,
        query: str | None = None,
        document_ids: list[str] | None = None,
        metadata_filters: dict | None = None,
        limit: int = 10,
    ):

        self.query = query

        self.document_ids = (
            document_ids or []
        )

        self.metadata_filters = (
            metadata_filters or {}
        )

        self.limit = limit