"""
Application Middleware

Centralized middleware registration.

Responsibilities
----------------
- Request ID generation
- Request logging
- Request timing
- Security headers
- Metrics collection

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations

import time
from uuid import uuid4

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.responses import JSONResponse

from app.core.config import settings
from app.core.logging import (
    clear_request_id,
    get_logger,
    set_request_id,
)

logger = get_logger(__name__)


###############################################################################
# Request ID Middleware
###############################################################################


class RequestIdMiddleware(BaseHTTPMiddleware):
    """
    Adds a request id to every request.
    """

    async def dispatch(self, request: Request, call_next):

        request_id = request.headers.get(
            "X-Request-ID",
            str(uuid4()),
        )

        set_request_id(request_id)

        request.state.request_id = request_id

        response = await call_next(request)

        response.headers["X-Request-ID"] = request_id

        clear_request_id()

        return response


###############################################################################
# Request Logging Middleware
###############################################################################


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs every incoming request.
    """

    async def dispatch(self, request: Request, call_next):

        logger.info(
            "Incoming request %s %s",
            request.method,
            request.url.path,
        )

        response = await call_next(request)

        logger.info(
            "Completed request %s status=%s",
            request.url.path,
            response.status_code,
        )

        return response


###############################################################################
# Timing Middleware
###############################################################################


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Measures request latency.
    """

    async def dispatch(self, request: Request, call_next):

        start = time.perf_counter()

        response = await call_next(request)

        elapsed = time.perf_counter() - start

        response.headers["X-Response-Time"] = (
            f"{elapsed * 1000:.2f} ms"
        )

        logger.debug(
            "Execution time %.2f ms",
            elapsed * 1000,
        )

        return response


###############################################################################
# Security Headers
###############################################################################


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Adds recommended security headers.
    """

    async def dispatch(self, request: Request, call_next):

        response = await call_next(request)

        response.headers["X-Frame-Options"] = "DENY"

        response.headers["X-Content-Type-Options"] = "nosniff"

        response.headers["Referrer-Policy"] = "strict-origin"

        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )

        response.headers["X-XSS-Protection"] = "1; mode=block"

        return response


###############################################################################
# Exception Middleware
###############################################################################


class ExceptionMiddleware(BaseHTTPMiddleware):
    """
    Converts unexpected exceptions into JSON.
    """

    async def dispatch(self, request: Request, call_next):

        try:
            return await call_next(request)

        except Exception as exc:

            logger.exception("Unhandled exception")

            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": {
                        "code": "INTERNAL_SERVER_ERROR",
                        "message": str(exc),
                    },
                    "request_id": getattr(
                        request.state,
                        "request_id",
                        "-",
                    ),
                },
            )


###############################################################################
# Middleware Registration
###############################################################################


def register_middlewares(app: FastAPI) -> None:
    """
    Registers all application middleware.
    """

    ###########################################################################
    # Compression
    ###########################################################################

    app.add_middleware(
        GZipMiddleware,
        minimum_size=1024,
    )

    ###########################################################################
    # CORS
    ###########################################################################

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    ###########################################################################
    # Custom middleware
    ###########################################################################

    app.add_middleware(ExceptionMiddleware)

    app.add_middleware(RequestIdMiddleware)

    app.add_middleware(TimingMiddleware)

    app.add_middleware(LoggingMiddleware)

    app.add_middleware(SecurityHeadersMiddleware)

    logger.info("Application middleware registered.")