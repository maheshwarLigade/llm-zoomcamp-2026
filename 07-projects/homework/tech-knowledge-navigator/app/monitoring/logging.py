"""
Metadata Builder

Builds normalized metadata payloads
for RAG documents and chunks.


Responsibilities:

- Create document metadata
- Create chunk metadata
- Add tenant information
- Add source information
- Add security attributes
- Normalize metadata structure


Metadata is stored with:

- Vector database payload
- Search index documents
- Audit records


Pipeline:

Document
    |
    v
MetadataBuilder
    |
    v
Metadata Payload
    |
    +------------+
    |            |
    v            v

Vector DB     Search Index


Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import logging


from dataclasses import dataclass, field


from datetime import datetime, timezone


from typing import Any



logger = logging.getLogger(__name__)



###############################################################################
# Models
###############################################################################


@dataclass
class MetadataContext:
    """
    Context information used while
    building metadata.
    """

    tenant_id: str | None = None

    user_id: str | None = None

    source_type: str | None = None

    source_url: str | None = None

    tags: list[str] = field(
        default_factory=list
    )

    permissions: list[str] = field(
        default_factory=list
    )



@dataclass
class DocumentMetadata:
    """
    Final document metadata.
    """

    document_id: str

    tenant_id: str | None

    source_type: str | None

    source_url: str | None

    tags: list[str]

    permissions: list[str]

    created_at: datetime

    extra: dict[str, Any] = field(
        default_factory=dict
    )



@dataclass
class ChunkMetadata:
    """
    Chunk level metadata.

    """

    document_id: str

    chunk_id: str

    chunk_index: int

    total_chunks: int

    page_number: int | None

    section: str | None

    extra: dict[str, Any] = field(
        default_factory=dict
    )



###############################################################################
# Configuration
###############################################################################


@dataclass
class MetadataBuilderConfig:
    """
    Metadata builder configuration.
    """

    include_timestamp: bool = True

    include_security: bool = True

    include_source: bool = True



###############################################################################
# Metadata Builder
###############################################################################


class MetadataBuilder:
    """
    Builds metadata payloads
    used by RAG components.

    """



    def __init__(
        self,
        config: MetadataBuilderConfig | None = None,
    ):

        self.config = (

            config

            or MetadataBuilderConfig()

        )



    ###########################################################################
    # Document Metadata
    ###########################################################################


    def build_document_metadata(
        self,
        document_id: str,
        context: MetadataContext,
        extra: dict | None = None,
    ) -> dict:
        """
        Build document metadata payload.
        """

        metadata = {

            "document_id":
                document_id,

            "tags":
                context.tags,

        }



        if self.config.include_source:

            metadata.update(

                {

                    "source_type":
                        context.source_type,

                    "source_url":
                        context.source_url,

                }

            )



        if context.tenant_id:

            metadata[

                "tenant_id"

            ] = context.tenant_id



        if self.config.include_security:

            metadata[

                "permissions"

            ] = context.permissions



        if self.config.include_timestamp:

            metadata[

                "created_at"

            ] = datetime.now(
                    timezone.utc
                ).isoformat()



        if extra:

            metadata.update(
                extra
            )



        return metadata



    ###########################################################################
    # Chunk Metadata
    ###########################################################################


    def build_chunk_metadata(
        self,
        document_id: str,
        chunk_id: str,
        chunk_index: int,
        total_chunks: int,
        page_number: int | None = None,
        section: str | None = None,
        extra: dict | None = None,
    ) -> dict:
        """
        Build chunk metadata.
        """

        metadata = {

            "document_id":
                document_id,

            "chunk_id":
                chunk_id,

            "chunk_index":
                chunk_index,

            "total_chunks":
                total_chunks,

        }



        if page_number is not None:

            metadata[

                "page_number"

            ] = page_number



        if section:

            metadata[

                "section"

            ] = section



        if extra:

            metadata.update(
                extra
            )



        return metadata



    ###########################################################################
    # Merge Metadata
    ###########################################################################


    def merge(
        self,
        *metadata_objects: dict,
    ) -> dict:
        """
        Merge multiple metadata objects.

        Later values override previous ones.
        """

        result = {}


        for item in metadata_objects:

            if item:

                result.update(
                    item
                )


        return result