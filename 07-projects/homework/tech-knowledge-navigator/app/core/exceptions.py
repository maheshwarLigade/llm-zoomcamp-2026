"""
Application Exceptions

Centralized exception hierarchy for the application.

Business services should raise these exceptions instead of
FastAPI HTTPException. The API layer converts them into HTTP
responses using global exception handlers.

Author
------
Tech Knowledge Navigator
"""

from typing import Any
from typing import Optional


###############################################################################
# Base Exception
###############################################################################


class ApplicationException(Exception):
    """
    Base class for all application exceptions.
    """

    def __init__(
        self,
        message: str,
        *,
        error_code: str = "APPLICATION_ERROR",
        status_code: int = 500,
        details: Optional[Any] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details

        super().__init__(message)


###############################################################################
# Validation Exceptions
###############################################################################


class ValidationException(ApplicationException):
    """
    Invalid input supplied by the client.
    """

    def __init__(
        self,
        message: str = "Validation failed.",
        details: Optional[Any] = None,
    ):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=400,
            details=details,
        )


###############################################################################
# Authentication / Authorization
###############################################################################


class AuthenticationException(ApplicationException):
    """
    Authentication failure.
    """

    def __init__(
        self,
        message: str = "Authentication failed.",
    ):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_FAILED",
            status_code=401,
        )


class AuthorizationException(ApplicationException):
    """
    User lacks permissions.
    """

    def __init__(
        self,
        message: str = "Permission denied.",
    ):
        super().__init__(
            message=message,
            error_code="ACCESS_DENIED",
            status_code=403,
        )


###############################################################################
# Resource Exceptions
###############################################################################


class ResourceNotFoundException(ApplicationException):
    """
    Resource not found.
    """

    def __init__(
        self,
        resource: str,
        identifier: Any,
    ):
        super().__init__(
            message=f"{resource} '{identifier}' not found.",
            error_code="RESOURCE_NOT_FOUND",
            status_code=404,
            details={
                "resource": resource,
                "identifier": identifier,
            },
        )


class ResourceAlreadyExistsException(ApplicationException):
    """
    Resource already exists.
    """

    def __init__(
        self,
        resource: str,
    ):
        super().__init__(
            message=f"{resource} already exists.",
            error_code="RESOURCE_ALREADY_EXISTS",
            status_code=409,
        )


###############################################################################
# Search Exceptions
###############################################################################


class SearchException(ApplicationException):
    """
    Search failure.
    """

    def __init__(
        self,
        message: str = "Search failed.",
    ):
        super().__init__(
            message=message,
            error_code="SEARCH_ERROR",
            status_code=500,
        )


class RetrievalException(ApplicationException):
    """
    Retrieval pipeline failure.
    """

    def __init__(
        self,
        message: str = "Document retrieval failed.",
    ):
        super().__init__(
            message=message,
            error_code="RETRIEVAL_ERROR",
            status_code=500,
        )


class EmbeddingException(ApplicationException):
    """
    Embedding generation failure.
    """

    def __init__(
        self,
        message: str = "Embedding generation failed.",
    ):
        super().__init__(
            message=message,
            error_code="EMBEDDING_ERROR",
            status_code=500,
        )


class RerankingException(ApplicationException):
    """
    Re-ranking failure.
    """

    def __init__(
        self,
        message: str = "Document reranking failed.",
    ):
        super().__init__(
            message=message,
            error_code="RERANKING_ERROR",
            status_code=500,
        )


###############################################################################
# LLM Exceptions
###############################################################################


class LLMException(ApplicationException):
    """
    LLM provider failure.
    """

    def __init__(
        self,
        message: str = "LLM request failed.",
    ):
        super().__init__(
            message=message,
            error_code="LLM_ERROR",
            status_code=502,
        )


class PromptException(ApplicationException):
    """
    Prompt generation failure.
    """

    def __init__(
        self,
        message: str = "Prompt construction failed.",
    ):
        super().__init__(
            message=message,
            error_code="PROMPT_ERROR",
            status_code=500,
        )


###############################################################################
# Database Exceptions
###############################################################################


class DatabaseException(ApplicationException):
    """
    Database failure.
    """

    def __init__(
        self,
        message: str = "Database operation failed.",
    ):
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            status_code=500,
        )


###############################################################################
# Vector Store Exceptions
###############################################################################


class VectorStoreException(ApplicationException):
    """
    Vector database failure.
    """

    def __init__(
        self,
        message: str = "Vector store unavailable.",
    ):
        super().__init__(
            message=message,
            error_code="VECTOR_STORE_ERROR",
            status_code=500,
        )


###############################################################################
# Ingestion Exceptions
###############################################################################


class IngestionException(ApplicationException):
    """
    Document ingestion failure.
    """

    def __init__(
        self,
        message: str = "Document ingestion failed.",
    ):
        super().__init__(
            message=message,
            error_code="INGESTION_ERROR",
            status_code=500,
        )


###############################################################################
# Evaluation Exceptions
###############################################################################


class EvaluationException(ApplicationException):
    """
    Evaluation failure.
    """

    def __init__(
        self,
        message: str = "Evaluation failed.",
    ):
        super().__init__(
            message=message,
            error_code="EVALUATION_ERROR",
            status_code=500,
        )


###############################################################################
# Monitoring Exceptions
###############################################################################


class MonitoringException(ApplicationException):
    """
    Monitoring failure.
    """

    def __init__(
        self,
        message: str = "Monitoring operation failed.",
    ):
        super().__init__(
            message=message,
            error_code="MONITORING_ERROR",
            status_code=500,
        )


###############################################################################
# External Service Exceptions
###############################################################################


class ExternalServiceException(ApplicationException):
    """
    External dependency failure.
    """

    def __init__(
        self,
        service: str,
    ):
        super().__init__(
            message=f"{service} service is unavailable.",
            error_code="EXTERNAL_SERVICE_ERROR",
            status_code=503,
            details={"service": service},
        )


###############################################################################
# Rate Limiting
###############################################################################


class RateLimitExceededException(ApplicationException):
    """
    Rate limit exceeded.
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded.",
    ):
        super().__init__(
            message=message,
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429,
        )


###############################################################################
# Configuration
###############################################################################


class ConfigurationException(ApplicationException):
    """
    Invalid application configuration.
    """

    def __init__(
        self,
        message: str = "Application configuration error.",
    ):
        super().__init__(
            message=message,
            error_code="CONFIGURATION_ERROR",
            status_code=500,
        )