"""
Document Repository Interface

Defines persistence contract for Document entity.

This is a domain abstraction.
Concrete implementations belong to infrastructure layer.

Example implementations:

- SQLDocumentRepository
- MongoDocumentRepository
- DynamoDocumentRepository

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


from abc import ABC, abstractmethod


from typing import Optional


from app.entities.document import (
    Document,
    DocumentStatus,
)



###############################################################################
# Repository Interface
###############################################################################


class DocumentRepository(
    ABC
):
    """
    Repository contract for Document aggregate.

    Responsibilities:

    - Save documents
    - Retrieve documents
    - Update lifecycle state
    - Search documents
    - Manage document metadata

    """


    ###########################################################################
    # Create / Update
    ###########################################################################


    @abstractmethod
    async def save(
        self,
        document: Document,
    ) -> Document:
        """
        Persist document.

        If document exists:
            update

        Otherwise:
            create
        """

        raise NotImplementedError



    @abstractmethod
    async def update(
        self,
        document: Document,
    ) -> Document:
        """
        Update existing document.
        """

        raise NotImplementedError



    ###########################################################################
    # Read Operations
    ###########################################################################


    @abstractmethod
    async def find_by_id(
        self,
        document_id: str,
    ) -> Optional[Document]:
        """
        Find document by identifier.
        """

        raise NotImplementedError



    @abstractmethod
    async def find_all(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Document]:
        """
        Retrieve documents with pagination.
        """

        raise NotImplementedError



    ###########################################################################
    # Search Operations
    ###########################################################################


    @abstractmethod
    async def search(
        self,
        query: str,
        limit: int = 10,
    ) -> list[Document]:
        """
        Search documents.

        Implementation may use:

        - Full text search
        - Metadata search
        - Keyword search
        """

        raise NotImplementedError



    @abstractmethod
    async def find_by_title(
        self,
        title: str,
    ) -> Optional[Document]:
        """
        Find document by title.
        """

        raise NotImplementedError



    ###########################################################################
    # Lifecycle Operations
    ###########################################################################


    @abstractmethod
    async def update_status(
        self,
        document_id: str,
        status: DocumentStatus,
        error_message: str | None = None,
    ) -> None:
        """
        Update document processing state.

        Example:

        PROCESSING
              |
              |
           INDEXED

        """

        raise NotImplementedError



    @abstractmethod
    async def delete(
        self,
        document_id: str,
    ) -> bool:
        """
        Delete document.

        Returns:

        True:
            deleted successfully

        False:
            document not found

        """

        raise NotImplementedError



    ###########################################################################
    # Existence Checks
    ###########################################################################


    @abstractmethod
    async def exists(
        self,
        document_id: str,
    ) -> bool:
        """
        Check document existence.
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
        Return total documents count.
        """

        raise NotImplementedError



    ###########################################################################
    # Retrieval Support
    ###########################################################################


    @abstractmethod
    async def find_searchable_documents(
        self,
        limit: int = 100,
    ) -> list[Document]:
        """
        Return documents available for retrieval.

        Only documents with:

            status = INDEXED

        should be returned.

        """

        raise NotImplementedError



###############################################################################
# Repository Specification Helpers
###############################################################################


class DocumentSpecification:
    """
    Query specification helper.

    Used for dynamic filtering.

    Example:

    - owner_id
    - document_type
    - status
    - created date

    """


    def __init__(
        self,
        filters: dict | None = None,
    ):

        self.filters = filters or {}



    def matches(
        self,
        document: Document,
    ) -> bool:
        """
        Check whether document satisfies filters.
        """

        for key, value in self.filters.items():

            if getattr(
                document,
                key,
                None,
            ) != value:

                return False


        return True