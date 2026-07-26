"""
Reranking Service

Responsible for improving retrieval quality by
reordering retrieved candidates based on
query relevance.

Pipeline:

Retriever
    |
    |
Candidate Chunks
    |
    |
Reranker
    |
    |
High Quality Context
    |
    |
LLM


Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import logging


from dataclasses import dataclass, field


from typing import Protocol, Any


from app.entities.chunk import Chunk


from app.domain.services.retrieval_service import (
    RetrievalResult,
)



logger = logging.getLogger(__name__)



###############################################################################
# External Contracts
###############################################################################


class RerankingModel(Protocol):
    """
    Contract for reranking models.

    Implementations:

    - Cohere Rerank
    - Cross Encoder
    - BGE Reranker
    - LLM Reranker
    """

    async def score(
        self,
        query: str,
        documents: list[str],
    ) -> list[float]:
        """
        Returns relevance scores.

        Example:

        [
            0.95,
            0.82,
            0.35
        ]

        """
        ...



###############################################################################
# Request / Response Models
###############################################################################


@dataclass
class RerankingRequest:
    """
    Reranking input.
    """

    query: str

    candidates: list[RetrievalResult]

    top_k: int = 5

    remove_duplicates: bool = True

    diversity_enabled: bool = False



@dataclass
class RerankingResult:
    """
    Final reranked chunk.
    """

    chunk: Chunk

    original_score: float

    rerank_score: float

    final_score: float

    rank: int

    metadata: dict[str, Any] = field(
        default_factory=dict
    )



@dataclass
class RerankingResponse:
    """
    Complete reranking response.
    """

    results: list[RerankingResult]

    total_candidates: int



###############################################################################
# Reranking Service
###############################################################################


class RerankingService:
    """
    Domain service responsible for
    retrieval result optimization.

    """



    def __init__(
        self,
        reranking_model: RerankingModel,
    ):

        self.reranking_model = (
            reranking_model
        )



    ###########################################################################
    # Public API
    ###########################################################################


    async def rerank(
        self,
        request: RerankingRequest,
    ) -> RerankingResponse:
        """
        Execute reranking pipeline.

        Steps:

        1. Remove duplicates
        2. Score candidates
        3. Combine scores
        4. Sort
        5. Return top K

        """

        candidates = (
            request.candidates
        )


        if request.remove_duplicates:

            candidates = (
                self._remove_duplicates(
                    candidates
                )
            )



        scores = await (
            self._calculate_scores(
                request.query,
                candidates,
            )
        )


        results = []


        for index, item in enumerate(
            candidates
        ):

            rerank_score = scores[index]


            final_score = (
                self._combine_scores(
                    item.score,
                    rerank_score,
                )
            )


            results.append(

                RerankingResult(

                    chunk=item.chunk,

                    original_score=item.score,

                    rerank_score=rerank_score,

                    final_score=final_score,

                    rank=0,

                )

            )



        results.sort(
            key=lambda x: x.final_score,
            reverse=True,
        )


        for index, result in enumerate(
            results,
            start=1,
        ):

            result.rank = index



        results = results[
            : request.top_k
        ]



        logger.info(
            "Reranked %s candidates",
            len(results),
        )



        return RerankingResponse(

            results=results,

            total_candidates=len(
                candidates
            ),

        )



    ###########################################################################
    # Scoring
    ###########################################################################


    async def _calculate_scores(
        self,
        query: str,
        candidates: list[RetrievalResult],
    ) -> list[float]:
        """
        Generate relevance scores.
        """

        documents = [

            item.chunk.content

            for item in candidates

        ]


        return await (
            self.reranking_model.score(
                query,
                documents,
            )
        )



    ###########################################################################
    # Score Fusion
    ###########################################################################


    def _combine_scores(
        self,
        retrieval_score: float,
        rerank_score: float,
    ) -> float:
        """
        Combine retrieval and reranking scores.

        Formula:

        final =
          30% retrieval
          +
          70% reranker

        """

        return (

            (retrieval_score * 0.3)

            +

            (rerank_score * 0.7)

        )



    ###########################################################################
    # Duplicate Handling
    ###########################################################################


    def _remove_duplicates(
        self,
        candidates: list[RetrievalResult],
    ) -> list[RetrievalResult]:
        """
        Remove duplicate chunks.

        """

        seen = set()

        unique = []


        for item in candidates:

            content_hash = hash(
                item.chunk.content
            )


            if content_hash not in seen:

                seen.add(
                    content_hash
                )

                unique.append(
                    item
                )


        return unique



    ###########################################################################
    # Context Builder
    ###########################################################################


    def build_context(
        self,
        response: RerankingResponse,
    ) -> str:
        """
        Build LLM context from
        reranked chunks.
        """

        return "\n\n".join(

            result.chunk.content

            for result in response.results

        )