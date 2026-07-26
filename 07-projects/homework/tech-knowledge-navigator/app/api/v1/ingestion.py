"""
Ingestion API

Provides endpoints for managing the document ingestion pipeline.

Responsibilities
----------------
* Trigger ingestion
* Monitor ingestion
* Retry failed ingestion
* Cancel ingestion
* List ingestion jobs
* Delete ingestion jobs
* Ingestion statistics

Business logic is delegated to IngestionService.
"""

from datetime import datetime
from enum import Enum
from typing import List
from typing import Optional
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from fastapi import status

from pydantic import BaseModel
from pydantic import Field

from app.api.deps import get_ingestion_service
from app.services.ingestion_service import IngestionService

router = APIRouter(
    prefix="/ingestion",
    tags=["Ingestion"],
)

###############################################################################
# Enums
###############################################################################


class IngestionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


###############################################################################
# Request Models
###############################################################################


class IngestionRequest(BaseModel):
    """
    Start ingestion request.
    """

    dataset_name: str = Field(
        ...,
        description="Dataset identifier.",
    )

    source_path: str = Field(
        ...,
        description="Input directory or file.",
    )

    chunk_size: int = Field(
        default=512,
        ge=128,
        le=4096,
    )

    chunk_overlap: int = Field(
        default=64,
        ge=0,
        le=512,
    )

    embedding_model: str = Field(
        default="BAAI/bge-small-en-v1.5",
    )

    recreate_index: bool = False

    enable_hybrid_search: bool = True

    enable_metadata_extraction: bool = True


###############################################################################
# Response Models
###############################################################################


class IngestionJobResponse(BaseModel):
    """
    Represents an ingestion job.
    """

    job_id: UUID

    dataset_name: str

    status: IngestionStatus

    started_at: datetime

    completed_at: Optional[datetime] = None

    processed_documents: int

    processed_chunks: int

    failed_documents: int

    message: str


class IngestionListResponse(BaseModel):
    """
    Paginated ingestion jobs.
    """

    total: int

    page: int

    page_size: int

    jobs: List[IngestionJobResponse]


class IngestionStatistics(BaseModel):
    """
    Overall ingestion statistics.
    """

    total_jobs: int

    completed_jobs: int

    running_jobs: int

    failed_jobs: int

    total_documents: int

    total_chunks: int


###############################################################################
# Start Ingestion
###############################################################################


@router.post(
    "",
    response_model=IngestionJobResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Start Ingestion",
)
async def start_ingestion(
    request: IngestionRequest,
    service: IngestionService = Depends(get_ingestion_service),
):
    """
    Starts a new ingestion job.
    """

    return await service.start_ingestion(request)


###############################################################################
# List Jobs
###############################################################################


@router.get(
    "",
    response_model=IngestionListResponse,
    summary="List Ingestion Jobs",
)
async def list_jobs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    service: IngestionService = Depends(get_ingestion_service),
):
    """
    Returns paginated ingestion jobs.
    """

    return await service.list_jobs(
        page=page,
        page_size=page_size,
    )


###############################################################################
# Job Details
###############################################################################


@router.get(
    "/{job_id}",
    response_model=IngestionJobResponse,
    summary="Get Ingestion Job",
)
async def get_job(
    job_id: UUID,
    service: IngestionService = Depends(get_ingestion_service),
):
    """
    Returns ingestion job details.
    """

    job = await service.get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingestion job not found.",
        )

    return job


###############################################################################
# Cancel Job
###############################################################################


@router.post(
    "/{job_id}/cancel",
    summary="Cancel Ingestion",
)
async def cancel_job(
    job_id: UUID,
    service: IngestionService = Depends(get_ingestion_service),
):
    """
    Cancels a running ingestion job.
    """

    cancelled = await service.cancel_job(job_id)

    if not cancelled:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found or cannot be cancelled.",
        )

    return {
        "status": "SUCCESS",
        "message": "Ingestion cancelled."
    }


###############################################################################
# Retry Job
###############################################################################


@router.post(
    "/{job_id}/retry",
    response_model=IngestionJobResponse,
    summary="Retry Ingestion",
)
async def retry_job(
    job_id: UUID,
    service: IngestionService = Depends(get_ingestion_service),
):
    """
    Retries a failed ingestion job.
    """

    return await service.retry_job(job_id)


###############################################################################
# Delete Job
###############################################################################


@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Ingestion Job",
)
async def delete_job(
    job_id: UUID,
    service: IngestionService = Depends(get_ingestion_service),
):
    """
    Deletes an ingestion job record.
    """

    deleted = await service.delete_job(job_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found.",
        )


###############################################################################
# Statistics
###############################################################################


@router.get(
    "/statistics/summary",
    response_model=IngestionStatistics,
    summary="Ingestion Statistics",
)
async def statistics(
    service: IngestionService = Depends(get_ingestion_service),
):
    """
    Returns ingestion statistics.
    """

    return await service.get_statistics()