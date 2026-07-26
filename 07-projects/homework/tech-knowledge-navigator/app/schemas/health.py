"""
Health API Schemas

Pydantic models used for application health,
readiness, liveness, and dependency monitoring.

Author
------
Tech Knowledge Navigator
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel
from pydantic import Field
from pydantic import ConfigDict


###############################################################################
# Health Status
###############################################################################


class HealthStatus(str, Enum):
    """
    Overall service status.
    """

    HEALTHY = "healthy"

    DEGRADED = "degraded"

    UNHEALTHY = "unhealthy"



###############################################################################
# Component Status
###############################################################################


class ComponentStatus(str, Enum):
    """
    Individual dependency status.
    """

    UP = "up"

    DOWN = "down"

    UNKNOWN = "unknown"



###############################################################################
# Dependency Health
###############################################################################


class DependencyHealth(BaseModel):
    """
    Health information for external dependencies.

    Example:
    - PostgreSQL
    - Qdrant
    - OpenSearch
    - Ollama
    """

    name: str = Field(
        ...,
        examples=[
            "postgres",
            "qdrant",
            "opensearch",
        ],
    )

    status: ComponentStatus

    response_time_ms: float | None = None

    message: str | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )



###############################################################################
# Application Health
###############################################################################


class HealthResponse(BaseModel):
    """
    Basic application health response.

    Endpoint:
        GET /health
    """

    status: HealthStatus

    service: str

    version: str

    environment: str

    timestamp: datetime

    uptime_seconds: float

    model_config = ConfigDict(
        from_attributes=True,
    )



###############################################################################
# Readiness Check
###############################################################################


class ReadinessResponse(BaseModel):
    """
    Kubernetes readiness probe response.

    Endpoint:
        GET /health/ready
    """

    status: HealthStatus

    ready: bool

    dependencies: list[DependencyHealth]

    timestamp: datetime



###############################################################################
# Liveness Check
###############################################################################


class LivenessResponse(BaseModel):
    """
    Kubernetes liveness probe response.

    Endpoint:
        GET /health/live
    """

    status: HealthStatus

    alive: bool

    timestamp: datetime



###############################################################################
# Detailed Health Check
###############################################################################


class DetailedHealthResponse(BaseModel):
    """
    Complete health information.

    Used by:
    - Admin dashboard
    - Monitoring
    - Debugging
    """

    status: HealthStatus

    application: HealthResponse

    dependencies: list[DependencyHealth]

    system: dict[str, Any] = Field(
        default_factory=dict,
    )

    timestamp: datetime



###############################################################################
# Dependency Check Request
###############################################################################


class DependencyCheckRequest(BaseModel):
    """
    Manual dependency check request.

    Used internally or by admin tools.
    """

    dependencies: list[str]



###############################################################################
# Health Metrics
###############################################################################


class HealthMetrics(BaseModel):
    """
    Runtime health metrics.

    Exposed for monitoring dashboards.
    """

    cpu_usage_percent: float | None = None

    memory_usage_percent: float | None = None

    active_connections: int = 0

    active_requests: int = 0

    average_response_time_ms: float | None = None

    total_requests: int = 0

    failed_requests: int = 0



###############################################################################
# Health Dashboard
###############################################################################


class HealthDashboardResponse(BaseModel):
    """
    Dashboard health response.

    Used by monitoring UI.
    """

    status: HealthStatus

    metrics: HealthMetrics

    dependencies: list[DependencyHealth]

    alerts: list[str] = Field(
        default_factory=list,
    )

    timestamp: datetime



###############################################################################
# Standard API Wrapper
###############################################################################


class HealthApiResponse(BaseModel):
    """
    Generic health API response wrapper.
    """

    success: bool = True

    data: HealthResponse

    request_id: str

    timestamp: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )