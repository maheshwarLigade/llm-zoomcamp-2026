"""
Monitoring API

Provides runtime metrics, application statistics, and operational
monitoring endpoints for the RAG application.

Responsibilities
----------------
* Runtime metrics
* Application statistics
* Retrieval statistics
* LLM statistics
* Feedback metrics
* System health summary
* Prometheus metrics endpoint

Business logic is delegated to MonitoringService.
"""

from datetime import datetime
from typing import Dict
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client import generate_latest
from pydantic import BaseModel

from app.api.deps import get_monitoring_service
from app.services.monitoring_service import MonitoringService

router = APIRouter(
    prefix="/monitoring",
    tags=["Monitoring"],
)

###############################################################################
# Response Models
###############################################################################


class RuntimeStatistics(BaseModel):
    uptime_seconds: int
    started_at: datetime

    total_requests: int
    successful_requests: int
    failed_requests: int

    average_latency_ms: float

    requests_per_minute: float

    active_sessions: int


class RetrievalStatistics(BaseModel):
    total_queries: int

    hybrid_queries: int

    vector_queries: int

    keyword_queries: int

    average_retrieval_time_ms: float

    average_documents_retrieved: float

    cache_hit_rate: float


class LLMStatistics(BaseModel):
    total_requests: int

    total_tokens: int

    prompt_tokens: int

    completion_tokens: int

    average_response_time_ms: float

    average_prompt_length: int

    average_completion_length: int

    model_usage: Dict[str, int]


class FeedbackStatistics(BaseModel):
    total_feedback: int

    positive_feedback: int

    negative_feedback: int

    neutral_feedback: int

    average_rating: float


class MonitoringSummary(BaseModel):
    runtime: RuntimeStatistics

    retrieval: RetrievalStatistics

    llm: LLMStatistics

    feedback: FeedbackStatistics


###############################################################################
# Monitoring Summary
###############################################################################


@router.get(
    "/summary",
    response_model=MonitoringSummary,
    summary="Monitoring Summary",
)
async def monitoring_summary(
    service: MonitoringService = Depends(get_monitoring_service),
):
    """
    Returns complete monitoring summary.
    """

    return await service.summary()


###############################################################################
# Runtime Metrics
###############################################################################


@router.get(
    "/runtime",
    response_model=RuntimeStatistics,
    summary="Runtime Statistics",
)
async def runtime_statistics(
    service: MonitoringService = Depends(get_monitoring_service),
):
    """
    Runtime metrics.
    """

    return await service.runtime_statistics()


###############################################################################
# Retrieval Metrics
###############################################################################


@router.get(
    "/retrieval",
    response_model=RetrievalStatistics,
    summary="Retrieval Statistics",
)
async def retrieval_statistics(
    service: MonitoringService = Depends(get_monitoring_service),
):
    """
    Retrieval metrics.
    """

    return await service.retrieval_statistics()


###############################################################################
# LLM Metrics
###############################################################################


@router.get(
    "/llm",
    response_model=LLMStatistics,
    summary="LLM Statistics",
)
async def llm_statistics(
    service: MonitoringService = Depends(get_monitoring_service),
):
    """
    LLM metrics.
    """

    return await service.llm_statistics()


###############################################################################
# Feedback Metrics
###############################################################################


@router.get(
    "/feedback",
    response_model=FeedbackStatistics,
    summary="Feedback Statistics",
)
async def feedback_statistics(
    service: MonitoringService = Depends(get_monitoring_service),
):
    """
    Feedback metrics.
    """

    return await service.feedback_statistics()


###############################################################################
# Prometheus Metrics
###############################################################################


@router.get(
    "/metrics",
    response_class=PlainTextResponse,
    include_in_schema=False,
)
async def prometheus_metrics():
    """
    Prometheus scrape endpoint.

    Example

    scrape_configs:
      - job_name: rag-api
        static_configs:
          - targets:
              - localhost:8000
    """

    return PlainTextResponse(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


###############################################################################
# Dashboard Statistics
###############################################################################


@router.get(
    "/dashboard",
    summary="Dashboard Statistics",
)
async def dashboard(
    service: MonitoringService = Depends(get_monitoring_service),
):
    """
    Dashboard statistics.

    Used by the Streamlit monitoring dashboard.
    """

    return await service.dashboard()


###############################################################################
# Application Information
###############################################################################


@router.get(
    "/info",
    summary="Application Information",
)
async def application_information(
    service: MonitoringService = Depends(get_monitoring_service),
):
    """
    Returns application metadata.
    """

    return await service.application_information()


###############################################################################
# Top Queries
###############################################################################


@router.get(
    "/top-queries",
    response_model=List[str],
    summary="Top User Queries",
)
async def top_queries(
    service: MonitoringService = Depends(get_monitoring_service),
):
    """
    Most frequent user queries.
    """

    return await service.top_queries(limit=20)