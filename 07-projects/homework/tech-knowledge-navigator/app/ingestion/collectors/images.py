"""
Image Collector

Collects image-based knowledge sources
for multimodal RAG ingestion.

Supported sources:

- Image URLs
- Document embedded images
- Screenshots
- Diagrams
- Scanned images


Pipeline:

Image Source
      |
      v
ImageCollector
      |
      v
Image Metadata
      |
      +----------------+
      |                |
      v                v
OCR Processing    Vision Model
      |
      v
Text / Image Embedding
      |
      v
Vector Store


Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import logging


from dataclasses import dataclass, field


from datetime import datetime


from typing import Protocol


from urllib.parse import urlparse



logger = logging.getLogger(__name__)



###############################################################################
# External Contracts
###############################################################################


class ImageDownloader(Protocol):
    """
    Downloads image content.

    Implementations:

    - httpx
    - aiohttp
    - S3 client

    """

    async def download(
        self,
        url: str,
    ) -> bytes:
        ...



class ImageAnalyzer(Protocol):
    """
    Optional image analyzer.

    Used for:

    - OCR
    - Caption generation
    - Image understanding

    """

    async def analyze(
        self,
        image_bytes: bytes,
    ) -> dict:
        ...



###############################################################################
# Models
###############################################################################


@dataclass
class ImageSource:
    """
    Image input source.
    """

    url: str

    filename: str | None = None

    document_id: str | None = None

    tags: list[str] = field(
        default_factory=list
    )



@dataclass
class ImageMetadata:
    """
    Image information.
    """

    filename: str | None

    content_type: str | None

    size_bytes: int

    width: int | None = None

    height: int | None = None

    checksum: str | None = None



@dataclass
class CollectedImage:
    """
    Collector output.
    """

    source: ImageSource

    content: bytes

    metadata: ImageMetadata

    collected_at: datetime

    analysis: dict = field(
        default_factory=dict
    )



###############################################################################
# Configuration
###############################################################################


@dataclass
class ImageCollectorConfig:
    """
    Image collector settings.
    """

    max_size_mb: int = 20

    allowed_extensions: list[str] = field(

        default_factory=lambda: [

            ".png",

            ".jpg",

            ".jpeg",

            ".webp",

            ".gif",

        ]

    )



###############################################################################
# Image Collector
###############################################################################


class ImageCollector:
    """
    Collects image resources.

    """



    def __init__(
        self,
        downloader: ImageDownloader,
        analyzer: ImageAnalyzer | None = None,
        config: ImageCollectorConfig | None = None,
    ):

        self.downloader = downloader

        self.analyzer = analyzer

        self.config = (

            config

            or ImageCollectorConfig()

        )



    ###########################################################################
    # Public API
    ###########################################################################


    async def collect(
        self,
        source: ImageSource,
    ) -> CollectedImage:
        """
        Collect image from source.
        """

        self._validate_url(
            source.url
        )


        logger.info(

            "Collecting image: %s",

            source.url,

        )


        image_bytes = await (

            self.downloader.download(

                source.url

            )

        )


        self._validate_size(
            image_bytes
        )



        metadata = ImageMetadata(

            filename=source.filename,

            content_type=self._detect_type(
                source.url
            ),

            size_bytes=len(
                image_bytes
            ),

        )



        analysis = {}



        if self.analyzer:

            analysis = await (

                self.analyzer.analyze(

                    image_bytes

                )

            )



        return CollectedImage(

            source=source,

            content=image_bytes,

            metadata=metadata,

            collected_at=datetime.utcnow(),

            analysis=analysis,

        )



    ###########################################################################
    # Batch Collection
    ###########################################################################


    async def collect_many(
        self,
        sources: list[ImageSource],
    ) -> list[CollectedImage]:
        """
        Collect multiple images.
        """

        results = []


        for source in sources:

            try:

                image = await (

                    self.collect(
                        source
                    )

                )

                results.append(
                    image
                )


            except Exception:

                logger.exception(

                    "Failed collecting image %s",

                    source.url,

                )



        return results



    ###########################################################################
    # Validation
    ###########################################################################


    def _validate_url(
        self,
        url: str,
    ):
        """
        Validate image URL.
        """

        parsed = urlparse(
            url
        )


        if not parsed.scheme:

            raise ValueError(
                "Invalid image URL"
            )


        if not parsed.netloc:

            raise ValueError(
                "Missing image domain"
            )



    def _validate_size(
        self,
        content: bytes,
    ):
        """
        Validate image size.
        """

        size_mb = (

            len(content)

            /

            (1024 * 1024)

        )


        if size_mb > self.config.max_size_mb:

            raise ValueError(

                f"Image exceeds maximum size {self.config.max_size_mb}MB"

            )



    ###########################################################################
    # Helpers
    ###########################################################################


    def _detect_type(
        self,
        url: str,
    ) -> str | None:
        """
        Detect image type from URL.
        """

        lower = url.lower()


        for extension in self.config.allowed_extensions:

            if lower.endswith(extension):

                return extension.replace(
                    ".",
                    "",
                )


        return None