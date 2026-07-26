"""
Evaluation API

Provides endpoints for evaluating the Retrieval-Augmented
Generation (RAG) pipeline.

Responsibilities
----------------
* Retrieval evaluation
* LLM evaluation
* End-to-end evaluation
* Hybrid search comparison
* Re-ranking evaluation
* Query rewriting evaluation
* Benchmark execution

Business logic is delegated to EvaluationService.
"""

from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from pydantic import BaseModel
from pydantic import Field

from app.api.deps import get_evaluation_service
from app.services.evaluation_service import EvaluationService

router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"],
)


###############################################################################
# Request Models
###############################################################################


class EvaluationRequest(BaseModel):
    """
    Generic evaluation request.
    """

    dataset: str = Field(
        ...,
        description="Evaluation dataset name",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=50,
    )

    use_hybrid_search: bool = True

    use_reranker: bool = True

    rewrite_query: bool = True

    llm_model: Optional[str] = None


###############################################################################
# Response Models
###############################################################################


class Metric(BaseModel):
    """
    Individual metric.
    """

    name: str

    value: float


class EvaluationResponse(BaseModel):
    """
    Generic evaluation response.
    """

    evaluation_id: UUID

    evaluation_type: str

    started_at: datetime

    completed_at: datetime

    metrics: List[Metric]

    metadata: Dict[str, Any]


class BenchmarkResponse(BaseModel):
    """
    Benchmark execution summary.
    """

    benchmark_id: UUID

    total_queries: int

    average_latency_ms: float

    throughput_qps: float

    success_rate: float

    completed_at: datetime


###############################################################################
# Retrieval Evaluation
###############################################################################


@router.post(
    "/retrieval",
    response_model=EvaluationResponse,
    summary="Evaluate Retrieval",
)
async def evaluate_retrieval(
    request: EvaluationRequest,
    service: EvaluationService = Depends(get_evaluation_service),
):
    """
    Evaluate retrieval quality.

    Metrics

    - Recall@K
    - Precision@K
    - MRR
    - nDCG
    """

    return await service.evaluate_retrieval(request)


###############################################################################
# LLM Evaluation
###############################################################################


@router.post(
    "/llm",
    response_model=EvaluationResponse,
    summary="Evaluate LLM",
)
async def evaluate_llm(
    request: EvaluationRequest,
    service: EvaluationService = Depends(get_evaluation_service),
):
    """
    Evaluate generated answers.

    Metrics

    - Faithfulness
    - Answer Relevancy
    - Context Recall
    - Context Precision
    """

    return await service.evaluate_llm(request)


###############################################################################
# Complete RAG Evaluation
###############################################################################


@router.post(
    "/rag",
    response_model=EvaluationResponse,
    summary="Evaluate Complete RAG Pipeline",
)
async def evaluate_rag(
    request: EvaluationRequest,
    service: EvaluationService = Depends(get_evaluation_service),
):
    """
    Executes complete RAG evaluation.
    """

    return await service.evaluate_rag(request)


###############################################################################
# Hybrid Search Comparison
###############################################################################


@router.post(
    "/hybrid-search",
    response_model=EvaluationResponse,
    summary="Compare Hybrid Search",
)
async def evaluate_hybrid_search(
    request: EvaluationRequest,
    service: EvaluationService = Depends(get_evaluation_service),
):
    """
    Compare BM25, Vector and Hybrid retrieval.
    """

    return await service.evaluate_hybrid_search(request)


###############################################################################
# Re-ranking Evaluation
###############################################################################


@router.post(
    "/reranker",
    response_model=EvaluationResponse,
    summary="Evaluate Re-ranking",
)
async def evaluate_reranker(
    request: EvaluationRequest,
    service: EvaluationService = Depends(get_evaluation_service),
):
    """
    Evaluate cross encoder re-ranking.
    """

    return await service.evaluate_reranker(request)


###############################################################################
# Query Rewriting Evaluation
###############################################################################


@router.post(
    "/query-rewriting",
    response_model=EvaluationResponse,
    summary="Evaluate Query Rewriting",
)
async def evaluate_query_rewriting(
    request: EvaluationRequest,
    service: EvaluationService = Depends(get_evaluation_service),
):
    """
    Evaluate rewritten queries.
    """

    return await service.evaluate_query_rewriting(request)


###############################################################################
# Benchmark
###############################################################################


@router.post(
    "/benchmark",
    response_model=BenchmarkResponse,
    summary="Run Benchmark",
)
async def benchmark(
    request: EvaluationRequest,
    service: EvaluationService = Depends(get_evaluation_service),
):
    """
    Executes performance benchmark.
    """

    return await service.run_benchmark(request)


###############################################################################
# Evaluation History
###############################################################################


@router.get(
    "",
    response_model=List[EvaluationResponse],
    summary="Evaluation History",
)
async def list_evaluations(
    limit: int = 20,
    service: EvaluationService = Depends(get_evaluation_service),
):
    """
    Returns previous evaluation runs.
    """

    return await service.list_evaluations(limit)


###############################################################################
# Evaluation Details
###############################################################################


@router.get(
    "/{evaluation_id}",
    response_model=EvaluationResponse,
    summary="Evaluation Details",
)
async def get_evaluation(
    evaluation_id: UUID,
    service: EvaluationService = Depends(get_evaluation_service),
):
    """
    Returns a single evaluation result.
    """

    evaluation = await service.get_evaluation(evaluation_id)

    if evaluation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluation not found.",
        )

    return evaluation