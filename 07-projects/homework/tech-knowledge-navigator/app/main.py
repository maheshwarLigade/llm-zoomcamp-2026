"""
FastAPI Application Entry Point

Main application bootstrap file.

Responsibilities:
- Create FastAPI app
- Register routers
- Configure middleware
- Configure lifecycle
- Register exception handlers

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException


from app.api.router import api_router

from app.core.config import settings

from app.core.lifespan import lifespan

from app.core.logging import configure_logging

from app.core.middleware import (
    RequestLoggingMiddleware,
    TimingMiddleware,
)



###############################################################################
# Initialize Logging
###############################################################################


configure_logging()



###############################################################################
# Create Application
###############################################################################


app = FastAPI(
    title=settings.APP_NAME,

    description="""
    Knowledge Navigator API

    Enterprise RAG application supporting:

    - Document ingestion
    - Hybrid search
    - Query rewriting
    - Document reranking
    - LLM generation
    - Evaluation
    - User feedback
    - Monitoring
    """,

    version=settings.APP_VERSION,

    docs_url="/docs",

    redoc_url="/redoc",

    lifespan=lifespan,
)



###############################################################################
# Middleware
###############################################################################


app.add_middleware(
    CORSMiddleware,

    allow_origins=settings.CORS_ORIGINS,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)



app.add_middleware(
    RequestLoggingMiddleware,
)


app.add_middleware(
    TimingMiddleware,
)



###############################################################################
# API Routers
###############################################################################


app.include_router(
    api_router,
    prefix="/api",
)



###############################################################################
# Root Endpoint
###############################################################################


@app.get(
    "/",
    tags=["System"],
)
async def root():
    """
    Application information.
    """

    return {
        "application": settings.APP_NAME,

        "version": settings.APP_VERSION,

        "environment": settings.ENVIRONMENT,

        "status": "running",
    }



###############################################################################
# Exception Handlers
###############################################################################


@app.exception_handler(
    HTTPException
)
async def http_exception_handler(
    request,
    exc,
):
    """
    Handle HTTP exceptions.
    """

    return {
        "success": False,

        "error": {
            "status_code": exc.status_code,

            "message": exc.detail,
        },
    }



@app.exception_handler(
    RequestValidationError
)
async def validation_exception_handler(
    request,
    exc,
):
    """
    Handle request validation errors.
    """

    return {
        "success": False,

        "error": {
            "type": "validation_error",

            "details": exc.errors(),
        },
    }



###############################################################################
# Startup Information
###############################################################################


@app.get(
    "/info",
    tags=["System"],
)
async def application_info():
    """
    Application metadata.
    """

    return {

        "name": settings.APP_NAME,

        "version": settings.APP_VERSION,

        "environment": settings.ENVIRONMENT,

        "features": [

            "rag",

            "hybrid-search",

            "query-rewriting",

            "reranking",

            "evaluation",

            "feedback",

            "monitoring",

        ],

    }