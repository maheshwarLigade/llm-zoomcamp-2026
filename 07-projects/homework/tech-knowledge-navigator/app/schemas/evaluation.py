"""
Evaluation API Schemas

Pydantic models used for retrieval evaluation,
LLM evaluation, benchmark execution, and RAG quality metrics.

Author
------
Tech Knowledge Navigator
"""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


###############################################################################
# Enums
###############################################################################


class EvaluationType(str, Enum):
    RETRIEVAL = "retrieval"
    LLM = "llm"
    RAGAS = "ragas"
    BENCHMARK = "benchmark"


###############################################################################
# Retrieval Evaluation
###############################################################################


class RetrievalEvaluationRequest(BaseModel):
    """
    Evaluate retrieval quality.
    """

    query: str = Field(..., min_length=2)

    expected_document_ids: list[str]

    retrieved_document_ids: list[str]

    top_k: int = 5


class RetrievalMetrics(BaseModel):
    """
    Retrieval quality metrics.
    """

    precision: float = Field(..., ge=0.0, le=1.0)

    recall: float = Field(..., ge=0.0, le=1.0)

    mrr: float = Field(..., ge=0.0, le=1.0)

    ndcg: float = Field(..., ge=0.0, le=1.0)

    hit_rate: float = Field(..., ge=0.0, le=1.0)


###############################################################################
# LLM Evaluation
###############################################################################


class LLMEvaluationRequest(BaseModel):
    """
    Evaluate generated answer.
    """

    question: str

    answer: str

    reference_answer: str | None = None

    context: list[str]


class LLMMetrics(BaseModel):
    """
    LLM quality metrics.
    """

    correctness: float = Field(..., ge=0.0, le=1.0)

    relevance: float = Field(..., ge=0.0, le=1.0)

    coherence: float = Field(..., ge=0.0, le=1.0)

    fluency: float = Field(..., ge=0.0, le=1.0)

    hallucination_score: float = Field(..., ge=0.0, le=1.0)


###############################################################################
# RAGAS Metrics
###############################################################################


class RagasMetrics(BaseModel):
    """
    Standard RAGAS evaluation metrics.
    """

    faithfulness: float = Field(..., ge=0.0, le=1.0)

    answer_relevancy: float = Field(..., ge=0.0, le=1.0)

    context_precision: float = Field(..., ge=0.0, le=1.0)

    context_recall: float = Field(..., ge=0.0, le=1.0)


###############################################################################
# Benchmark
###############################################################################


class BenchmarkRequest(BaseModel):
    """
    Execute benchmark suite.
    """

    dataset_name: str

    embedding_model: str

    llm_model: str

    reranker_enabled: bool = True

    hybrid_search: bool = True

    query_rewriting: bool = True


class BenchmarkResult(BaseModel):
    """
    Benchmark execution result.
    """

    execution_time_ms: float

    total_questions: int

    successful_questions: int

    failed_questions: int

    average_latency_ms: float

    average_score: float


###############################################################################
# Evaluation Summary
###############################################################################


class EvaluationSummary(BaseModel):
    """
    Combined evaluation summary.
    """

    retrieval: RetrievalMetrics | None = None

    llm: LLMMetrics | None = None

    ragas: RagasMetrics | None = None

    benchmark: BenchmarkResult | None = None


###############################################################################
# Evaluation Response
###############################################################################


class EvaluationResponse(BaseModel):
    """
    Evaluation response.
    """

    evaluation_id: UUID = Field(default_factory=uuid4)

    evaluation_type: EvaluationType

    dataset: str

    model: str

    summary: EvaluationSummary

    metadata: dict[str, Any] = Field(default_factory=dict)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True)


###############################################################################
# Evaluation History
###############################################################################


class EvaluationHistoryItem(BaseModel):
    """
    Historical evaluation entry.
    """

    evaluation_id: UUID

    evaluation_type: EvaluationType

    model: str

    score: float

    created_at: datetime


class EvaluationHistoryResponse(BaseModel):
    """
    Evaluation history.
    """

    evaluations: list[EvaluationHistoryItem]

    total: int


###############################################################################
# Compare Experiments
###############################################################################


class ExperimentComparisonRequest(BaseModel):
    """
    Compare multiple evaluation runs.
    """

    evaluation_ids: list[UUID]


class ExperimentComparisonResponse(BaseModel):
    """
    Experiment comparison.
    """

    winner: UUID

    experiments: list[EvaluationResponse]


###############################################################################
# Generic API Response
###############################################################################


class EvaluationApiResponse(BaseModel):
    """
    Standard API response.
    """

    success: bool = True

    data: EvaluationResponse

    request_id: str

    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True)