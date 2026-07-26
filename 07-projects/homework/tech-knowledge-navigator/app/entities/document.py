"""
Document Domain Entity

Represents a knowledge document inside
the RAG system.

Responsibilities:
- Manage document lifecycle
- Track ingestion status
- Maintain document metadata
- Associate chunks
- Support retrieval filtering

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
# Document Status
###############################################################################


class DocumentStatus(str, Enum):
    """
    Document processing lifecycle.
    """

    CREATED = "created"

    UPLOADED = "uploaded"

    PROCESSING = "processing"

    INDEXED = "indexed"

    FAILED = "failed"

    ARCHIVED = "archived"



###############################################################################
# Document Type
###############################################################################


class DocumentType(str, Enum):
    """
    Supported document formats.
    """

    PDF = "pdf"

    MARKDOWN = "markdown"

    TEXT = "text"

    HTML = "html"

    CSV = "csv"

    DOCX = "docx"

    JSON = "json"



###############################################################################
# Document Source
###############################################################################


@dataclass
class DocumentSource:
    """
    Source information of document.

    Example:

    S3 bucket
    Local file
    URL
    Database
    """

    source_type: str

    location: str

    checksum: str | None = None



###############################################################################
# Document Entity
###############################################################################


@dataclass
class Document:
    """
    Document aggregate root.

    Example:

        Document

            |
            |
        +---+---+
        |       |
     Chunk1   Chunk2

    """


    ###########################################################################
    # Identity
    ###########################################################################

    id: str


    ###########################################################################
    # Basic Information
    ###########################################################################

    title: str


    description: str | None = None


    document_type: DocumentType = (
        DocumentType.TEXT
    )



    ###########################################################################
    # Ownership
    ###########################################################################

    owner_id: str | None = None



    ###########################################################################
    # Processing State
    ###########################################################################

    status: DocumentStatus = (
        DocumentStatus.CREATED
    )



    error_message: str | None = None



    ###########################################################################
    # Source Information
    ###########################################################################

    source: DocumentSource | None = None



    ###########################################################################
    # Content Statistics
    ###########################################################################

    total_pages: int = 0


    total_chunks: int = 0


    total_tokens: int = 0



    ###########################################################################
    # Chunk References
    ###########################################################################

    chunk_ids: list[str] = field(
        default_factory=list
    )



    ###########################################################################
    # Search Metadata
    ###########################################################################

    keywords: list[str] = field(
        default_factory=list
    )


    entities: list[str] = field(
        default_factory=list
    )



    ###########################################################################
    # Custom Metadata
    ###########################################################################

    metadata: dict[str, Any] = field(
        default_factory=dict
    )



    ###########################################################################
    # Versioning
    ###########################################################################

    version: int = 1



    ###########################################################################
    # Audit Information
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
    # Business Methods
    ###########################################################################


    def start_processing(
        self,
    ):
        """
        Mark document processing started.
        """

        self.status = (
            DocumentStatus.PROCESSING
        )

        self.updated_at = datetime.now(
            timezone.utc
        )



    def mark_indexed(
        self,
    ):
        """
        Mark document indexing completed.
        """

        self.status = (
            DocumentStatus.INDEXED
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
        Mark ingestion failure.
        """

        self.status = (
            DocumentStatus.FAILED
        )

        self.error_message = error

        self.updated_at = datetime.now(
            timezone.utc
        )



    def archive(
        self,
    ):
        """
        Archive document.
        """

        self.status = (
            DocumentStatus.ARCHIVED
        )

        self.updated_at = datetime.now(
            timezone.utc
        )



    ###########################################################################
    # Chunk Management
    ###########################################################################


    def add_chunk(
        self,
        chunk_id: str,
    ):
        """
        Associate chunk with document.
        """

        if chunk_id not in self.chunk_ids:

            self.chunk_ids.append(
                chunk_id
            )

            self.total_chunks = len(
                self.chunk_ids
            )



    def remove_chunk(
        self,
        chunk_id: str,
    ):
        """
        Remove chunk reference.
        """

        if chunk_id in self.chunk_ids:

            self.chunk_ids.remove(
                chunk_id
            )

            self.total_chunks = len(
                self.chunk_ids
            )



    ###########################################################################
    # Metadata Management
    ###########################################################################


    def add_keyword(
        self,
        keyword: str,
    ):
        """
        Add searchable keyword.
        """

        if keyword not in self.keywords:

            self.keywords.append(
                keyword
            )



    def add_entity(
        self,
        entity: str,
    ):
        """
        Add extracted entity.
        """

        if entity not in self.entities:

            self.entities.append(
                entity
            )



    def update_metadata(
        self,
        values: dict[str, Any],
    ):
        """
        Update metadata.
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
        Increment document version.
        """

        self.version += 1

        self.updated_at = datetime.now(
            timezone.utc
        )



    ###########################################################################
    # Helper Methods
    ###########################################################################


    def is_searchable(
        self,
    ) -> bool:
        """
        Check whether document can participate
        in retrieval.
        """

        return (
            self.status
            ==
            DocumentStatus.INDEXED
        )



    def to_metadata(
        self,
    ) -> dict[str, Any]:
        """
        Convert document metadata
        for vector database filtering.
        """

        return {

            "document_id": self.id,

            "title": self.title,

            "type": self.document_type.value,

            "owner_id": self.owner_id,

            "keywords": self.keywords,

            "entities": self.entities,

            "version": self.version,

        }



    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Serialize entity.
        """

        return {

            "id": self.id,

            "title": self.title,

            "description": self.description,

            "status": self.status.value,

            "document_type":
                self.document_type.value,

            "total_chunks":
                self.total_chunks,

            "total_tokens":
                self.total_tokens,

            "version":
                self.version,

            "created_at":
                self.created_at.isoformat(),

            "updated_at":
                self.updated_at.isoformat(),

        }