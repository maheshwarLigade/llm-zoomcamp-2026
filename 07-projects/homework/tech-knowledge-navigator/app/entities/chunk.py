"""
Chunk Domain Entity

Represents a document chunk used inside
the Retrieval Augmented Generation pipeline.

Responsibilities:
- Store chunk content
- Maintain document relationship
- Track chunk position
- Store token metadata
- Support retrieval and ranking

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


from dataclasses import dataclass, field

from datetime import datetime, timezone

from typing import Any



###############################################################################
# Chunk Type
###############################################################################


class ChunkType:
    """
    Chunk content types.
    """

    TEXT = "text"

    TABLE = "table"

    CODE = "code"

    IMAGE_DESCRIPTION = "image_description"



###############################################################################
# Chunk Entity
###############################################################################


@dataclass
class Chunk:
    """
    Domain representation of a document chunk.

    A chunk is the smallest searchable unit
    in the RAG pipeline.

    Example:

        Document
            |
            +-- Chunk 1
            |
            +-- Chunk 2
            |
            +-- Chunk 3

    """


    ###########################################################################
    # Identity
    ###########################################################################

    id: str


    document_id: str


    ###########################################################################
    # Content
    ###########################################################################

    content: str


    chunk_type: str = ChunkType.TEXT



    ###########################################################################
    # Position Information
    ###########################################################################

    chunk_index: int = 0


    page_number: int | None = None


    section_name: str | None = None



    ###########################################################################
    # Token Information
    ###########################################################################

    token_count: int = 0


    character_count: int = 0



    ###########################################################################
    # Embedding Information
    ###########################################################################

    embedding_id: str | None = None


    embedding_model: str | None = None



    ###########################################################################
    # Retrieval Metadata
    ###########################################################################

    metadata: dict[str, Any] = field(
        default_factory=dict
    )



    ###########################################################################
    # Search Optimization
    ###########################################################################

    keywords: list[str] = field(
        default_factory=list
    )


    entities: list[str] = field(
        default_factory=list
    )



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
    # Methods
    ###########################################################################


    def update_content(
        self,
        content: str,
    ):
        """
        Update chunk content
        and refresh metadata.
        """

        self.content = content

        self.character_count = len(
            content
        )

        self.updated_at = datetime.now(
            timezone.utc
        )



    def set_embedding(
        self,
        embedding_id: str,
        model: str,
    ):
        """
        Associate embedding information.
        """

        self.embedding_id = embedding_id

        self.embedding_model = model



    def add_keyword(
        self,
        keyword: str,
    ):
        """
        Add search keyword.
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
        Merge metadata.

        Example:

        {
          "source":"manual.pdf",
          "author":"John"
        }

        """

        self.metadata.update(
            values
        )


    def get_preview(
        self,
        length: int = 200,
    ) -> str:
        """
        Return short content preview.
        """

        if len(self.content) <= length:

            return self.content


        return (
            self.content[:length]
            +
            "..."
        )



    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Convert entity to dictionary.

        Useful for:
        - API response
        - Vector metadata
        - Serialization
        """

        return {

            "id": self.id,

            "document_id": self.document_id,

            "content": self.content,

            "chunk_type": self.chunk_type,

            "chunk_index": self.chunk_index,

            "page_number": self.page_number,

            "section_name": self.section_name,

            "token_count": self.token_count,

            "keywords": self.keywords,

            "entities": self.entities,

            "metadata": self.metadata,

        }