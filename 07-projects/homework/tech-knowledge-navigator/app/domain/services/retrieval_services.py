"""
Retrieval Service

Responsible for retrieving relevant knowledge
for Retrieval Augmented Generation.

Supports:

- Keyword retrieval
- Semantic retrieval
- Hybrid retrieval
- Metadata filtering
- Context preparation

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import logging


from dataclasses import dataclass, field


from typing import Protocol, Any


from app.entities.chunk import Chunk


from app.domain.repositories.chunk_repository import (
    ChunkRepository,
)



logger = logging.getLogger(__name__)



###############################################################################
# External Service Contracts
###############################################################################


class VectorSearchEngine(Protocol):
    """
    Contract for vector similarity search.

    Implementations:

    - Qdrant
    - Pinecone
    - Chroma
    - pgvector
    """

    async def search(
        self,
        query_embedding: list[float],
        limit: int,
        filters: dict[str, Any] | None = None,
    ) -> list[str]:
        """
        Returns chunk ids.
        """
        ...



class EmbeddingGenerator(Protocol):
    """
    Generates query embeddings.
    """

    async def generate(
        self,
        text: str,
    ) -> list[float]:
        ...



###############################################################################
# Request / Response Models
###############################################################################


@dataclass
class RetrievalRequest:
    """
    Retrieval input.
    """

    query: str

    top_k: int = 10

    use_keyword_search: bool = True

    use_vector_search: bool = True

    filters: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class RetrievalResult:
    """
    Single retrieved result.
    """

    chunk: Chunk

    score: float

    source: str = "unknown"

    retrieval_method: str = ""



@dataclass
class RetrievalResponse:
    """
    Complete retrieval response.
    """

    results: list[RetrievalResult]

    total_candidates: int

    retrieval_time_ms: float = 0



###############################################################################
# Retrieval Service
###############################################################################


class RetrievalService:
    """
    Domain service responsible for
    knowledge retrieval.

    """



    def __init__(
        self,
        chunk_repository: ChunkRepository,
        vector_search: VectorSearchEngine,
        embedding_generator: EmbeddingGenerator,
    ):

        self.chunk_repository = (
            chunk_repository
        )

        self.vector_search = (
            vector_search
        )

        self.embedding_generator = (
            embedding_generator
        )



    ###########################################################################
    # Main Retrieval API
    ###########################################################################


    async def retrieve(
        self,
        request: RetrievalRequest,
    ) -> RetrievalResponse:
        """
        Execute retrieval pipeline.

        Flow:

        Query

          |
          |
        Keyword Search

          +

        Vector Search

          |

        Merge Results

          |

        Return Candidates

        """

        import time


        start = time.perf_counter()


        candidates: dict[str, RetrievalResult] = {}



        #######################################################################
        # Keyword Retrieval
        #######################################################################

        if request.use_keyword_search:

            keyword_results = await (
                self._keyword_search(
                    request
                )
            )


            for result in keyword_results:

                candidates[
                    result.chunk.id
                ] = result



        #######################################################################
        # Semantic Retrieval
        #######################################################################

        if request.use_vector_search:

            vector_results = await (
                self._vector_search(
                    request
                )
            )


            for result in vector_results:

                existing = candidates.get(
                    result.chunk.id
                )


                if existing:

                    # Combine scores
                    existing.score = (
                        existing.score
                        +
                        result.score
                    )

                    existing.retrieval_method = (
                        "hybrid"
                    )

                else:

                    candidates[
                        result.chunk.id
                    ] = result



        results = list(
            candidates.values()
        )



        results.sort(
            key=lambda x: x.score,
            reverse=True,
        )



        results = results[
            : request.top_k
        ]



        elapsed = (
            time.perf_counter()
            -
            start
        )


        logger.info(
            "Retrieved %s chunks",
            len(results),
        )


        return RetrievalResponse(

            results=results,

            total_candidates=len(
                candidates
            ),

            retrieval_time_ms=(
                elapsed * 1000
            ),

        )



    ###########################################################################
    # Keyword Search
    ###########################################################################


    async def _keyword_search(
        self,
        request: RetrievalRequest,
    ) -> list[RetrievalResult]:
        """
        Execute keyword based retrieval.

        Usually backed by:

        - BM25
        - Elasticsearch
        - OpenSearch

        """

        chunks = await (
            self.chunk_repository
            .search_by_keyword(
                request.query,
                request.top_k,
            )
        )


        return [

            RetrievalResult(

                chunk=chunk,

                score=1.0,

                source="keyword",

                retrieval_method="keyword",

            )

            for chunk in chunks

        ]



    ###########################################################################
    # Vector Search
    ###########################################################################


    async def _vector_search(
        self,
        request: RetrievalRequest,
    ) -> list[RetrievalResult]:
        """
        Execute semantic search.
        """

        query_vector = await (
            self.embedding_generator.generate(
                request.query
            )
        )


        chunk_ids = await (
            self.vector_search.search(
                query_vector,
                request.top_k,
                request.filters,
            )
        )



        chunks = await (
            self.chunk_repository
            .find_by_ids(
                chunk_ids
            )
        )



        results = []


        for index, chunk in enumerate(chunks):

            score = (
                1.0
                -
                (index * 0.05)
            )


            results.append(

                RetrievalResult(

                    chunk=chunk,

                    score=score,

                    source="vector",

                    retrieval_method="semantic",

                )

            )


        return results



    ###########################################################################
    # Utility Methods
    ###########################################################################


    async def retrieve_context(
        self,
        query: str,
        limit: int = 5,
    ) -> str:
        """
        Build context string for LLM.

        Example:

        Chunk 1

        Chunk 2

        Chunk 3

        """

        response = await self.retrieve(

            RetrievalRequest(

                query=query,

                top_k=limit,

            )

        )


        return "\n\n".join(

            result.chunk.content

            for result in response.results

        )