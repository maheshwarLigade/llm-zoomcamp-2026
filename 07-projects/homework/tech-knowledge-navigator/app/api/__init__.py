"""
API Version 1

This package exposes the Version 1 router.

The router aggregates all endpoint modules for the first version
of the REST API.

Endpoints
---------
- Health
- Chat
- Retrieval
- Evaluation
- Feedback
- Monitoring
- Ingestion
- Administration

Example
-------
from app.api import api_v1_router
"""

from app.api.router import router as api_v1_router

__all__ = [
    "api_v1_router",
]