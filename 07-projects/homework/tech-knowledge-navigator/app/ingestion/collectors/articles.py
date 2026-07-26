"""
Article Collector

Collects article content from external sources.

Supported sources:

- Web articles
- Documentation pages
- Blog posts
- Knowledge base articles


Responsibilities:

1. Fetch article
2. Extract metadata
3. Return raw document


Pipeline:

URL
 |
 v
ArticleCollector
 |
 v
Raw Article
 |
 v
Extractor
 |
 v
Cleaner
 |
 v
Chunker


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


class HTTPClient(Protocol):
    """
    HTTP client abstraction.

    Implementations:

    - httpx
    - aiohttp

    """

    async def get(
        self,
        url: str,
        headers: dict[str, str] | None = None,
    ) -> str:
        ...



class ArticleExtractor(Protocol):
    """
    Extracts article information from HTML.

    """

    async def extract(
        self,
        html: str,
    ) -> "ArticleContent":
        ...



###############################################################################
# Models
###############################################################################


@dataclass
class ArticleSource:
    """
    Article input source.
    """

    url: str

    source_name: str | None = None

    tags: list[str] = field(
        default_factory=list
    )



@dataclass
class ArticleContent:
    """
    Extracted article content.
    """

    title: str

    content: str

    author: str | None = None

    published_date: datetime | None = None

    url: str | None = None

    metadata: dict = field(
        default_factory=dict
    )



@dataclass
class CollectedArticle:
    """
    Collector output.
    """

    source: ArticleSource

    article: ArticleContent

    collected_at: datetime

    metadata: dict = field(
        default_factory=dict
    )



###############################################################################
# Configuration
###############################################################################


@dataclass
class ArticleCollectorConfig:
    """
    Collector configuration.
    """

    timeout_seconds: int = 30

    user_agent: str = (
        "RAG-Knowledge-Collector/1.0"
    )

    allowed_domains: list[str] | None = None



###############################################################################
# Article Collector
###############################################################################


class ArticleCollector:
    """
    Collects article documents.

    """



    def __init__(
        self,
        http_client: HTTPClient,
        extractor: ArticleExtractor,
        config: ArticleCollectorConfig | None = None,
    ):

        self.http_client = http_client

        self.extractor = extractor

        self.config = (

            config

            or ArticleCollectorConfig()

        )



    ###########################################################################
    # Public API
    ###########################################################################


    async def collect(
        self,
        source: ArticleSource,
    ) -> CollectedArticle:
        """
        Collect article from URL.

        """

        self._validate_url(
            source.url
        )


        logger.info(
            "Collecting article: %s",
            source.url,
        )



        html = await self.http_client.get(

            source.url,

            headers={

                "User-Agent":
                    self.config.user_agent

            },

        )



        article = await (
            self.extractor.extract(
                html
            )
        )



        article.url = (
            source.url
        )



        return CollectedArticle(

            source=source,

            article=article,

            collected_at=datetime.utcnow(),

            metadata={

                "collector":
                    "article",

                "url":
                    source.url,

            },

        )



    ###########################################################################
    # Batch Collection
    ###########################################################################


    async def collect_many(
        self,
        sources: list[ArticleSource],
    ) -> list[CollectedArticle]:
        """
        Collect multiple articles.
        """

        results = []


        for source in sources:

            try:

                article = await (
                    self.collect(
                        source
                    )
                )


                results.append(
                    article
                )


            except Exception:

                logger.exception(

                    "Failed collecting %s",

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
        Validate article URL.
        """

        parsed = urlparse(
            url
        )


        if not parsed.scheme:

            raise ValueError(
                "Invalid URL"
            )


        if not parsed.netloc:

            raise ValueError(
                "Missing domain"
            )



        if self.config.allowed_domains:

            domain = parsed.netloc


            allowed = any(

                domain.endswith(
                    item
                )

                for item
                in self.config.allowed_domains

            )


            if not allowed:

                raise ValueError(
                    f"Domain not allowed: {domain}"
                )