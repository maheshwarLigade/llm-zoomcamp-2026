"""
PDF Collector

Collects PDF documents for RAG ingestion.

Responsibilities:

- Download PDF content
- Validate PDF format
- Validate size
- Extract document metadata
- Return raw PDF bytes


Pipeline:

PDF Source
     |
     v
PDFCollector
     |
     v
Raw PDF Document
     |
     v
PDF Extractor
     |
     v
PDF Cleaner
     |
     v
Chunking
     |
     v
Embedding


Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import hashlib

import logging


from dataclasses import dataclass, field


from datetime import datetime


from typing import Protocol


from urllib.parse import urlparse



logger = logging.getLogger(__name__)



###############################################################################
# External Contracts
###############################################################################


class PDFDownloader(Protocol):
    """
    Downloads PDF content.

    Implementations:

    - httpx
    - aiohttp
    - S3 client
    - Azure Blob client

    """

    async def download(
        self,
        source: str,
    ) -> bytes:
        ...



###############################################################################
# Models
###############################################################################


@dataclass
class PDFSource:
    """
    PDF input source.

    Source can be:

    - URL
    - S3 path
    - Internal storage reference
    """

    location: str

    filename: str | None = None

    document_id: str | None = None

    tags: list[str] = field(
        default_factory=list
    )

    metadata: dict = field(
        default_factory=dict
    )



@dataclass
class PDFMetadata:
    """
    PDF document metadata.
    """

    filename: str | None

    size_bytes: int

    checksum: str

    content_type: str

    page_count: int | None = None



@dataclass
class CollectedPDF:
    """
    Collector output.
    """

    source: PDFSource

    content: bytes

    metadata: PDFMetadata

    collected_at: datetime



###############################################################################
# Configuration
###############################################################################


@dataclass
class PDFCollectorConfig:
    """
    PDF collector configuration.
    """

    max_size_mb: int = 100

    validate_magic_bytes: bool = True

    allowed_content_types: list[str] = field(

        default_factory=lambda: [

            "application/pdf"

        ]

    )



###############################################################################
# PDF Collector
###############################################################################


class PDFCollector:
    """
    Collects PDF documents.

    """



    def __init__(
        self,
        downloader: PDFDownloader,
        config: PDFCollectorConfig | None = None,
    ):

        self.downloader = downloader


        self.config = (

            config

            or PDFCollectorConfig()

        )



    ###########################################################################
    # Public API
    ###########################################################################


    async def collect(
        self,
        source: PDFSource,
    ) -> CollectedPDF:
        """
        Collect PDF document.
        """

        logger.info(

            "Collecting PDF: %s",

            source.location,

        )


        content = await (

            self.downloader.download(

                source.location

            )

        )


        self._validate_size(
            content
        )


        if self.config.validate_magic_bytes:

            self._validate_pdf_signature(
                content
            )



        metadata = PDFMetadata(

            filename=source.filename,

            size_bytes=len(
                content
            ),

            checksum=self._checksum(
                content
            ),

            content_type="application/pdf",

        )



        return CollectedPDF(

            source=source,

            content=content,

            metadata=metadata,

            collected_at=datetime.utcnow(),

        )



    ###########################################################################
    # Batch Collection
    ###########################################################################


    async def collect_many(
        self,
        sources: list[PDFSource],
    ) -> list[CollectedPDF]:
        """
        Collect multiple PDFs.
        """

        results = []


        for source in sources:

            try:

                pdf = await (

                    self.collect(
                        source
                    )

                )

                results.append(
                    pdf
                )


            except Exception:

                logger.exception(

                    "Failed collecting PDF %s",

                    source.location,

                )



        return results



    ###########################################################################
    # Validation
    ###########################################################################


    def _validate_size(
        self,
        content: bytes,
    ):
        """
        Validate PDF size.
        """

        size_mb = (

            len(content)

            /

            (1024 * 1024)

        )


        if size_mb > self.config.max_size_mb:

            raise ValueError(

                f"PDF exceeds maximum size "
                f"{self.config.max_size_mb}MB"

            )



    def _validate_pdf_signature(
        self,
        content: bytes,
    ):
        """
        Validate PDF magic bytes.

        PDF files start with:

        %PDF-

        """

        if not content.startswith(
            b"%PDF-"
        ):

            raise ValueError(

                "Invalid PDF document"

            )



    ###########################################################################
    # Helpers
    ###########################################################################


    def _checksum(
        self,
        content: bytes,
    ) -> str:
        """
        Generate checksum.

        Used for:

        - Duplicate detection
        - Document versioning
        - Idempotent ingestion

        """

        return hashlib.sha256(
            content
        ).hexdigest()