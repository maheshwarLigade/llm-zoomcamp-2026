"""
Health Check API

Provides application health endpoints.

Endpoints
---------
GET /health
    Comprehensive application health.

GET /live
    Kubernetes liveness probe.

GET /ready
    Kubernetes readiness probe.

Author
------
Tech Knowledge Navigator
"""

from datetime import datetime
from typing import Dict

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel

from app.api.deps import get_health_service
from app.services.health_service import HealthService

router = APIRouter(
    tags=["Health"],
)

###############################################################################
# Response Models
###############################################################################


class ComponentHealth(BaseModel):
    """
    Health status for an individual component.
    """

    status: str
    message: str


class HealthResponse(BaseModel):
    """
    Complete application health response.
    """

    application: str

    version: str

    environment: str

    timestamp: datetime

    status: str

    components: Dict[str, ComponentHealth]


###############################################################################
# Health Endpoint
###############################################################################


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Application Health",
)
async def health(
    service: HealthService = Depends(get_health_service),
):
    """
    Returns complete application health.

    Checks

    - PostgreSQL
    - OpenSearch
    - Qdrant
    - LLM Provider
    """

    result = await service.health()

    if result.status != "UP":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=result.model_dump(),
        )

    return result


###############################################################################
# Liveness Probe
###############################################################################


@router.get(
    "/live",
    summary="Liveness Probe",
)
async def live():
    """
    Indicates that the application process is alive.

    This endpoint intentionally does not check external
    dependencies.
    """

    return {
        "status": "UP",
        "timestamp": datetime.utcnow(),
    }


###############################################################################
# Readiness Probe
###############################################################################


@router.get(
    "/ready",
    summary="Readiness Probe",
)
async def ready(
    service: HealthService = Depends(get_health_service),
):
    """
    Indicates whether the application is ready
    to receive requests.
    """

    ready = await service.ready()

    if not ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Application is not ready.",
        )

    return {
        "status": "READY",
        "timestamp": datetime.utcnow(),
    }