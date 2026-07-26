"""
Application Logging Configuration

Provides centralized logging configuration for the application.

Features
--------
- Console logging
- Rotating file logging
- Request ID support
- Structured logging
- Configurable log levels

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations

import contextvars
import logging
import logging.config
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import settings

###############################################################################
# Request Context
###############################################################################

request_id_context: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id",
    default="-",
)


###############################################################################
# Filters
###############################################################################


class RequestIdFilter(logging.Filter):
    """
    Injects request_id into every log record.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_context.get()
        return True


###############################################################################
# Formatter
###############################################################################


LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(request_id)s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


###############################################################################
# Logging Configuration
###############################################################################


def configure_logging() -> None:
    """
    Configures application logging.
    """

    log_directory = Path("logs")
    log_directory.mkdir(exist_ok=True)

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    request_filter = RequestIdFilter()

    ###########################################################################
    # Console
    ###########################################################################

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    console_handler.addFilter(request_filter)

    ###########################################################################
    # Application Log
    ###########################################################################

    application_handler = RotatingFileHandler(
        filename=log_directory / "application.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=10,
        encoding="utf-8",
    )

    application_handler.setFormatter(formatter)

    application_handler.addFilter(request_filter)

    ###########################################################################
    # Error Log
    ###########################################################################

    error_handler = RotatingFileHandler(
        filename=log_directory / "error.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=10,
        encoding="utf-8",
    )

    error_handler.setLevel(logging.ERROR)

    error_handler.setFormatter(formatter)

    error_handler.addFilter(request_filter)

    ###########################################################################
    # Root Logger
    ###########################################################################

    root_logger = logging.getLogger()

    root_logger.setLevel(settings.LOG_LEVEL.upper())

    root_logger.handlers.clear()

    root_logger.addHandler(console_handler)

    root_logger.addHandler(application_handler)

    root_logger.addHandler(error_handler)

    ###########################################################################
    # Third Party Libraries
    ###########################################################################

    logging.getLogger("uvicorn").setLevel(logging.INFO)

    logging.getLogger("uvicorn.access").setLevel(logging.INFO)

    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    logging.getLogger("httpx").setLevel(logging.WARNING)

    logging.getLogger("urllib3").setLevel(logging.WARNING)


###############################################################################
# Logger Factory
###############################################################################


def get_logger(name: str) -> logging.Logger:
    """
    Returns configured logger.

    Example
    -------
    logger = get_logger(__name__)
    """

    return logging.getLogger(name)


###############################################################################
# Request ID Utilities
###############################################################################


def set_request_id(request_id: str) -> None:
    """
    Sets request id for current request.
    """

    request_id_context.set(request_id)


def clear_request_id() -> None:
    """
    Clears current request id.
    """

    request_id_context.set("-")


###############################################################################
# Application Logger
###############################################################################

logger = get_logger("app")