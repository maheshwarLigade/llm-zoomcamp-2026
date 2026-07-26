"""
Evaluation Service

Responsible for evaluating RAG system quality.

Supports:

- Retrieval evaluation
- Answer evaluation
- Feedback analysis
- Benchmark generation
- Quality metrics

Evaluation dimensions:

1. Retrieval Quality
2. Generation Quality
3. User Satisfaction
4. Hallucination Detection


Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import logging


from dataclasses import dataclass, field


from typing import Protocol, Any


from app.domain.repositories.feedback_repository import (
    FeedbackRepository,
)


logger = logging.getLogger(__name__)



###############################################################################
# External Contracts
###############################################################################


class LLMJudge(Protocol):
    """
    LLM based evaluator.

    Used for:

    - Answer correctness
    - Faithfulness
    - Relevance

    Implementations:

    - GPT model
    - Claude
    - Gemini
    - Local LLM

    """

    async def evaluate(
        self,
        question: str,
        answer: str,
        context: str,
    ) -> dict[str, float]:
        """
        Returns evaluation scores.

        Example:

        {
            "faithfulness":0.92,
            "relevance":0.88
        }

        """
        ...



class RetrievalEvaluator(Protocol):
    """
    Evaluates retrieved documents.
    """

    async def evaluate(
        self,
        query: str,
        retrieved_chunks: list[str],
        expected_chunks: list[str] | None = None,
    ) -> dict[str, float]:
        ...



###############################################################################
# Request Models
###############################################################################


@dataclass
class EvaluationRequest:
    """
    Evaluation input.
    """

    question: str

    answer: str

    context: str

    expected_answer: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict
    )



@dataclass
class RetrievalEvaluationRequest:
    """
    Retrieval evaluation input.
    """

    query: str

    retrieved_chunks: list[str]

    expected_chunks: list[str] | None = None



###############################################################################
# Response Models
###############################################################################


@dataclass
class EvaluationResult:
    """
    Evaluation output.
    """

    faithfulness: float

    relevance: float

    correctness: float

    hallucination_score: float

    overall_score: float

    metadata: dict[str, Any] = field(
        default_factory=dict
    )



@dataclass
class RetrievalEvaluationResult:
    """
    Retrieval metrics.
    """

    precision: float

    recall: float

    hit_rate: float

    mrr: float



@dataclass
class EvaluationReport:
    """
    Complete evaluation report.
    """

    total_samples: int

    average_score: float

    metrics: dict[str, float]

    failed_cases: list[dict[str, Any]]



###############################################################################
# Evaluation Service
###############################################################################


class EvaluationService:
    """
    Domain service for RAG evaluation.

    """



    def __init__(
        self,
        feedback_repository: FeedbackRepository,
        llm_judge: LLMJudge,
        retrieval_evaluator: RetrievalEvaluator,
    ):

        self.feedback_repository = (
            feedback_repository
        )

        self.llm_judge = (
            llm_judge
        )

        self.retrieval_evaluator = (
            retrieval_evaluator
        )



    ###########################################################################
    # Answer Evaluation
    ###########################################################################


    async def evaluate_answer(
        self,
        request: EvaluationRequest,
    ) -> EvaluationResult:
        """
        Evaluate generated answer.

        Metrics:

        Faithfulness:
            Is answer supported by context?

        Relevance:
            Does answer answer question?

        Correctness:
            Is answer factually correct?

        Hallucination:
            Does answer contain unsupported claims?

        """

        scores = await (
            self.llm_judge.evaluate(

                question=request.question,

                answer=request.answer,

                context=request.context,

            )
        )


        faithfulness = scores.get(
            "faithfulness",
            0.0,
        )

        relevance = scores.get(
            "relevance",
            0.0,
        )

        correctness = scores.get(
            "correctness",
            0.0,
        )


        hallucination = (
            1.0 - faithfulness
        )


        overall = (
            (
                faithfulness
                +
                relevance
                +
                correctness
            )
            /
            3
        )


        return EvaluationResult(

            faithfulness=faithfulness,

            relevance=relevance,

            correctness=correctness,

            hallucination_score=hallucination,

            overall_score=overall,

            metadata=request.metadata,

        )



    ###########################################################################
    # Retrieval Evaluation
    ###########################################################################


    async def evaluate_retrieval(
        self,
        request: RetrievalEvaluationRequest,
    ) -> RetrievalEvaluationResult:
        """
        Evaluate retrieval quality.

        Metrics:

        Precision:
            Relevant results / retrieved results


        Recall:
            Found relevant documents


        MRR:
            Ranking quality

        """

        metrics = await (
            self.retrieval_evaluator.evaluate(

                query=request.query,

                retrieved_chunks=
                    request.retrieved_chunks,

                expected_chunks=
                    request.expected_chunks,

            )
        )


        return RetrievalEvaluationResult(

            precision=metrics.get(
                "precision",
                0,
            ),

            recall=metrics.get(
                "recall",
                0,
            ),

            hit_rate=metrics.get(
                "hit_rate",
                0,
            ),

            mrr=metrics.get(
                "mrr",
                0,
            ),

        )



    ###########################################################################
    # Feedback Based Evaluation
    ###########################################################################


    async def generate_feedback_report(
        self,
        limit: int = 1000,
    ) -> EvaluationReport:
        """
        Analyze production feedback.

        Used for:

        - Finding failures
        - Improving prompts
        - Improving retrieval

        """

        dataset = await (
            self.feedback_repository
            .get_evaluation_dataset(
                limit
            )
        )


        failed_cases = []


        total_score = 0


        for item in dataset:

            score = item.get(
                "rating",
                0,
            )


            total_score += score


            if score <= 2:

                failed_cases.append(
                    item
                )



        average = (

            total_score / len(dataset)

            if dataset

            else 0

        )



        return EvaluationReport(

            total_samples=len(dataset),

            average_score=average,

            metrics={

                "satisfaction":
                    average,

                "failure_rate":
                    (
                        len(failed_cases)
                        /
                        len(dataset)
                    )
                    if dataset
                    else 0,

            },

            failed_cases=failed_cases,

        )



    ###########################################################################
    # Benchmark Dataset
    ###########################################################################


    async def build_benchmark_dataset(
        self,
        limit: int = 1000,
    ) -> list[dict]:
        """
        Build evaluation benchmark dataset.

        Format:

        {
          question,
          context,
          answer,
          rating
        }

        """

        return await (
            self.feedback_repository
            .export_training_examples(
                limit
            )
        )



    ###########################################################################
    # Quality Gates
    ###########################################################################


    def passes_quality_gate(
        self,
        result: EvaluationResult,
        minimum_score: float = 0.75,
    ) -> bool:
        """
        Check if response quality
        is acceptable.

        """

        return (
            result.overall_score
            >=
            minimum_score
        )