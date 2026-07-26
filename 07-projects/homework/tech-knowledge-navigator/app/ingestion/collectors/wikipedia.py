"""
Wikipedia Collector

Collects Wikipedia articles for RAG ingestion.

Responsibilities:

- Fetch Wikipedia article
- Extract article metadata
- Capture revision information
- Support multiple languages
- Return structured article content


Supported:

- Wikipedia pages
- Wikipedia API
- Multiple languages


Pipeline:

Wikipedia API
      |
      v
WikipediaCollector
      |
      v
WikipediaArticle
      |
      v
Cleaner
      |
      v
Chunker
      |
      v
Embedding


Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import logging


from dataclasses import dataclass, field


from datetime import datetime


from typing import Protocol


logger = logging.getLogger(__name__)



###############################################################################
# External Contracts
###############################################################################


class WikipediaClient(Protocol):
    """
    Wikipedia API client abstraction.

    Possible implementations:

    - wikipedia-api
    - httpx wrapper
    - MediaWiki API client

    """

    async def fetch_article(
        self,
        title: str,
        language: str,
    ) -> dict:
        ...



###############################################################################
# Models
###############################################################################


@dataclass
class WikipediaSource:
    """
    Wikipedia article source.
    """

    title: str

    language: str = "en"

    category: str | None = None

    tags: list[str] = field(
        default_factory=list
    )



@dataclass
class WikipediaArticle:
    """
    Wikipedia article content.
    """

    title: str

    content: str

    language: str

    url: str | None = None

    summary: str | None = None

    categories: list[str] = field(
        default_factory=list
    )

    references: list[str] = field(
        default_factory=list
    )

    revision_id: str | None = None



@dataclass
class CollectedWikipediaArticle:
    """
    Collector output.
    """

    source: WikipediaSource

    article: WikipediaArticle

    collected_at: datetime

    metadata: dict = field(
        default_factory=dict
    )



###############################################################################
# Configuration
###############################################################################


@dataclass
class WikipediaCollectorConfig:
    """
    Collector configuration.
    """

    default_language: str = "en"

    include_references: bool = True

    include_categories: bool = True

    include_summary: bool = True



###############################################################################
# Wikipedia Collector
###############################################################################


class WikipediaCollector:
    """
    Collects Wikipedia articles.

    """



    def __init__(
        self,
        client: WikipediaClient,
        config: WikipediaCollectorConfig | None = None,
    ):

        self.client = client


        self.config = (

            config

            or WikipediaCollectorConfig()

        )



    ###########################################################################
    # Public API
    ###########################################################################


    async def collect(
        self,
        source: WikipediaSource,
    ) -> CollectedWikipediaArticle:
        """
        Collect Wikipedia article.
        """

        language = (

            source.language

            or

            self.config.default_language

        )


        logger.info(

            "Collecting Wikipedia article: %s (%s)",

            source.title,

            language,

        )



        response = await (

            self.client.fetch_article(

                title=source.title,

                language=language,

            )

        )



        article = WikipediaArticle(

            title=response.get(
                "title",
                source.title,
            ),

            content=response.get(
                "content",
                "",
            ),

            language=language,

            url=response.get(
                "url"
            ),

            summary=(

                response.get(
                    "summary"
                )

                if self.config.include_summary

                else None

            ),

            categories=(

                response.get(
                    "categories",
                    []

                )

                if self.config.include_categories

                else []

            ),

            references=(

                response.get(
                    "references",
                    []

                )

                if self.config.include_references

                else []

            ),

            revision_id=response.get(
                "revision_id"
            ),

        )



        return CollectedWikipediaArticle(

            source=source,

            article=article,

            collected_at=datetime.utcnow(),

            metadata={

                "collector":
                    "wikipedia",

                "language":
                    language,

                "title":
                    source.title,

            },

        )



    ###########################################################################
    # Batch Collection
    ###########################################################################


    async def collect_many(
        self,
        sources: list[WikipediaSource],
    ) -> list[CollectedWikipediaArticle]:
        """
        Collect multiple Wikipedia pages.
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

                    "Failed collecting Wikipedia page %s",

                    source.title,

                )



        return results