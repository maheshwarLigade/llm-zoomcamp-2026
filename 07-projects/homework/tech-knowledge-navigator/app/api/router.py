"""
Root API Router

This module is responsible for registering all API versions.

Current Versions
----------------
- v1

Future
------
- v2
- v3

The application only imports this router in main.py.

Example
-------
app.include_router(api_router)
"""

from fastapi import APIRouter

from app.api.v1 import api_v1_router

api_router = APIRouter()

# ------------------------------------------------------------------
# API Version 1
# ------------------------------------------------------------------

api_router.include_router(
    api_v1_router,
    prefix="/api/v1",
    tags=["API v1"],
)