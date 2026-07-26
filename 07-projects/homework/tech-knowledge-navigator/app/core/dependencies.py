"""
Application Dependencies

Centralized dependency injection for FastAPI.

Responsibilities
----------------
- Configuration
- Database Session
- Search Service
- Chat Service
- Document Service
- Ingestion Service
- Evaluation Service
- Monitoring Service
- Feedback Service
- Health Service

Author
------
Tech Knowledge Navigator
"""

from collections.abc import Generator
from uuid import uuid4

from fastapi import Header
from fastapi import HTTPException
from fastapi import Request
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal

from app.services.chat_service import ChatService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.evaluation_service import EvaluationService
from app.services.feedback_service import FeedbackService
from app.services.health_service import HealthService
from app.services.ingestion_service import IngestionService
from app.services.llm_service import LLMService
from app.services.monitoring_service import MonitoringService
from app.services.reranker_service import RerankerService
from app.services.search_service import SearchService
from app.services.vector_store_service import VectorStoreService


###############################################################################
# Configuration
###############################################################################


def get_settings():
    """
    Returns application settings.
    """
    return settings


###############################################################################
# Database
###############################################################################


def get_db() -> Generator[Session, None, None]:
    """
    Provides SQLAlchemy session.

    Session is automatically closed after request.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


###############################################################################
# Infrastructure Services
###############################################################################


def get_embedding_service() -> EmbeddingService:
    """
    Embedding model service.
    """
    return EmbeddingService()


def get_vector_store_service() -> VectorStoreService:
    """
    Qdrant/OpenSearch abstraction.
    """
    return VectorStoreService()


def get_reranker_service() -> RerankerService:
    """
    Cross encoder reranker.
    """
    return RerankerService()


def get_llm_service() -> LLMService:
    """
    LLM provider abstraction.
    """
    return LLMService()


###############################################################################
# Business Services
###############################################################################


def get_search_service(
    embedding_service: EmbeddingService = get_embedding_service(),
    vector_store: VectorStoreService = get_vector_store_service(),
    reranker: RerankerService = get_reranker_service(),
) -> SearchService:
    """
    Search service.
    """

    return SearchService(
        embedding_service=embedding_service,
        vector_store=vector_store,
        reranker=reranker,
    )


def get_chat_service(
    llm_service: LLMService = get_llm_service(),
    search_service: SearchService = get_search_service(),
) -> ChatService:
    """
    Chat service.
    """

    return ChatService(
        llm_service=llm_service,
        search_service=search_service,
    )


def get_document_service() -> DocumentService:
    """
    Document service.
    """

    return DocumentService()


def get_ingestion_service() -> IngestionService:
    """
    Ingestion pipeline service.
    """

    return IngestionService()


def get_evaluation_service() -> EvaluationService:
    """
    Evaluation service.
    """

    return EvaluationService()


def get_feedback_service() -> FeedbackService:
    """
    Feedback service.
    """

    return FeedbackService()


def get_monitoring_service() -> MonitoringService:
    """
    Monitoring service.
    """

    return MonitoringService()


def get_health_service() -> HealthService:
    """
    Health service.
    """

    return HealthService()


###############################################################################
# Request Context
###############################################################################


def get_request_id(
    x_request_id: str | None = Header(default=None),
) -> str:
    """
    Returns request id.

    Generates one if the client didn't provide it.
    """

    return x_request_id or str(uuid4())


###############################################################################
# Authentication
###############################################################################


def get_current_user(
    authorization: str | None = Header(default=None),
):
    """
    Placeholder authentication dependency.

    Replace with OAuth2/JWT implementation.
    """

    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required.",
        )

    return {
        "user_id": "demo-user",
        "username": "demo",
        "roles": ["USER"],
    }


###############################################################################
# Admin Dependency
###############################################################################


def require_admin(
    user= get_current_user(),
):
    """
    Requires administrator role.
    """

    if "ADMIN" not in user["roles"]:
        raise HTTPException(
            status_code=403,
            detail="Administrator privileges required.",
        )

    return user


###############################################################################
# Request Context Helper
###############################################################################


def get_client_ip(request: Request) -> str:
    """
    Returns client IP address.
    """

    if request.client:
        return request.client.host

    return "unknown"