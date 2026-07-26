"""
YouTube Collector

Collects YouTube video knowledge
for RAG ingestion.

Responsibilities:

- Validate YouTube URL
- Fetch video metadata
- Fetch transcript
- Capture channel information
- Prepare document payload


Pipeline:

YouTube Video
      |
      v
YouTubeCollector
      |
      v
Transcript + Metadata
      |
      v
Text Cleaner
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


import logging


import re


from dataclasses import dataclass, field


from datetime import datetime


from typing import Protocol


from urllib.parse import urlparse, parse_qs



logger = logging.getLogger(__name__)



###############################################################################
# External Contracts
###############################################################################


class YouTubeClient(Protocol):
    """
    YouTube API abstraction.

    Implementations:

    - YouTube Data API
    - youtube-transcript-api wrapper
    - Internal API client

    """

    async def get_video_metadata(
        self,
        video_id: str,
    ) -> dict:
        ...


    async def get_transcript(
        self,
        video_id: str,
        language: str,
    ) -> list[dict]:
        ...



###############################################################################
# Models
###############################################################################


@dataclass
class YouTubeSource:
    """
    YouTube video source.
    """

    url: str

    language: str = "en"

    tags: list[str] = field(
        default_factory=list
    )



@dataclass
class YouTubeTranscript:
    """
    Transcript information.
    """

    text: str

    language: str

    duration_seconds: float



@dataclass
class YouTubeVideo:
    """
    YouTube video content.
    """

    video_id: str

    title: str

    description: str

    channel_name: str | None

    published_at: datetime | None

    transcript: YouTubeTranscript | None

    url: str



@dataclass
class CollectedYouTubeVideo:
    """
    Collector output.
    """

    source: YouTubeSource

    video: YouTubeVideo

    collected_at: datetime

    metadata: dict = field(
        default_factory=dict
    )



###############################################################################
# Configuration
###############################################################################


@dataclass
class YouTubeCollectorConfig:
    """
    YouTube collector configuration.
    """

    default_language: str = "en"

    include_description: bool = True

    include_transcript: bool = True

    max_transcript_length: int = 500000



###############################################################################
# Collector
###############################################################################


class YouTubeCollector:
    """
    Collects YouTube videos.

    """



    def __init__(
        self,
        client: YouTubeClient,
        config: YouTubeCollectorConfig | None = None,
    ):

        self.client = client

        self.config = (

            config

            or YouTubeCollectorConfig()

        )



    ###########################################################################
    # Public API
    ###########################################################################


    async def collect(
        self,
        source: YouTubeSource,
    ) -> CollectedYouTubeVideo:
        """
        Collect YouTube video.
        """

        video_id = self._extract_video_id(
            source.url
        )


        logger.info(

            "Collecting YouTube video %s",

            video_id,

        )


        metadata = await (

            self.client.get_video_metadata(

                video_id

            )

        )



        transcript = None



        if self.config.include_transcript:

            transcript_data = await (

                self.client.get_transcript(

                    video_id,

                    source.language,

                )

            )


            transcript = (

                self._build_transcript(

                    transcript_data,

                    source.language,

                )

            )



        video = YouTubeVideo(

            video_id=video_id,

            title=metadata.get(
                "title",
                "",
            ),

            description=(

                metadata.get(
                    "description",
                    ""
                )

                if self.config.include_description

                else ""

            ),

            channel_name=metadata.get(
                "channel_name"
            ),

            published_at=metadata.get(
                "published_at"
            ),

            transcript=transcript,

            url=source.url,

        )



        return CollectedYouTubeVideo(

            source=source,

            video=video,

            collected_at=datetime.utcnow(),

            metadata={

                "collector":
                    "youtube",

                "video_id":
                    video_id,

            },

        )



    ###########################################################################
    # Batch Collection
    ###########################################################################


    async def collect_many(
        self,
        sources: list[YouTubeSource],
    ) -> list[CollectedYouTubeVideo]:
        """
        Collect multiple videos.
        """

        results = []


        for source in sources:

            try:

                result = await (

                    self.collect(
                        source
                    )

                )

                results.append(
                    result
                )


            except Exception:

                logger.exception(

                    "Failed collecting YouTube video %s",

                    source.url,

                )


        return results



    ###########################################################################
    # Helpers
    ###########################################################################


    def _extract_video_id(
        self,
        url: str,
    ) -> str:
        """
        Extract video ID.

        Supports:

        https://youtube.com/watch?v=id

        https://youtu.be/id

        """

        parsed = urlparse(
            url
        )


        if "youtu.be" in parsed.netloc:

            return parsed.path.strip("/")



        query = parse_qs(
            parsed.query
        )


        if "v" in query:

            return query["v"][0]



        raise ValueError(
            "Invalid YouTube URL"
        )



    def _build_transcript(
        self,
        items: list[dict],
        language: str,
    ) -> YouTubeTranscript:
        """
        Convert transcript segments
        into text.
        """

        text_parts = []

        duration = 0.0


        for item in items:

            text_parts.append(

                item.get(
                    "text",
                    ""
                )

            )


            duration += (

                item.get(
                    "duration",
                    0
                )

            )


        text = " ".join(
            text_parts
        )



        if len(text) > self.config.max_transcript_length:

            text = text[
                :
                self.config.max_transcript_length
            ]



        return YouTubeTranscript(

            text=text,

            language=language,

            duration_seconds=duration,

        )