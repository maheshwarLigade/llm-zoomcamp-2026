"""
Application Lifespan Management

Handles startup and shutdown events for the FastAPI application.

Responsibilities
----------------
- Validate configuration
- Initialize database
- Connect OpenSearch
- Connect Qdrant
- Validate LLM provider
- Warm up embedding model
- Initialize monitoring
- Graceful shutdown
- Resource cleanup

Author
------
Tech Knowledge Navigator
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import get_logger
from app.db.session import init_db, close_db
from app.services.vector_store_service import VectorStoreService
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.monitoring_service import MonitoringService

logger = get_logger(__name__)


###############################################################################
# Startup Helpers
###############################################################################


async def validate_configuration() -> None:
    """
    Validate application configuration.
    """

    logger.info("Validating application configuration...")

    if settings.LLM_PROVIDER == "openai" and not settings.OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY is required when using OpenAI provider."
        )

    logger.info("Configuration validated successfully.")


async def initialize_database() -> None:
    """
    Initialize database connection.
    """

    logger.info("Initializing PostgreSQL connection...")

    await init_db()

    logger.info("Database initialized successfully.")


async def initialize_vector_store() -> None:
    """
    Initialize OpenSearch and Qdrant connections.
    """

    logger.info("Initializing vector stores...")

    vector_store = VectorStoreService()

    await vector_store.connect()

    logger.info("Vector stores initialized successfully.")


async def initialize_llm() -> None:
    """
    Validate LLM provider connectivity.
    """

    logger.info("Initializing LLM provider...")

    llm = LLMService()

    await llm.health_check()

    logger.info("LLM provider initialized successfully.")


async def warmup_models() -> None:
    """
    Warm up embedding and reranking models.
    """

    logger.info("Warming up models...")

    embedding_service = EmbeddingService()

    # Trigger lazy model loading
    await embedding_service.embed_query("warmup")

    logger.info("Models warmed up successfully.")


async def initialize_monitoring() -> None:
    """
    Initialize metrics and monitoring.
    """

    logger.info("Initializing monitoring...")

    monitoring = MonitoringService()

    monitoring.initialize_metrics()

    logger.info("Monitoring initialized successfully.")


###############################################################################
# Shutdown Helpers
###############################################################################


async def shutdown_vector_store() -> None:
    """
    Close vector store connections.
    """

    logger.info("Closing vector store connections...")

    vector_store = VectorStoreService()

    await vector_store.close()

    logger.info("Vector store connections closed.")


async def shutdown_database() -> None:
    """
    Close database connections.
    """

    logger.info("Closing database connections...")

    await close_db()

    logger.info("Database connections closed.")


###############################################################################
# Lifespan
###############################################################################


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager.

    Startup Sequence
    ----------------
    1. Validate configuration
    2. Initialize database
    3. Initialize vector stores
    4. Initialize LLM provider
    5. Warm up models
    6. Initialize monitoring

    Shutdown Sequence
    -----------------
    1. Close vector stores
    2. Close database
    """

    logger.info("Starting %s v%s", settings.APP_NAME, settings.APP_VERSION)

    try:
        await validate_configuration()
        await initialize_database()
        await initialize_vector_store()
        await initialize_llm()
        await warmup_models()
        await initialize_monitoring()

        logger.info("Application startup completed successfully.")

        yield

    except Exception as exc:
        logger.exception("Application startup failed: %s", exc)
        raise

    finally:
        logger.info("Shutting down application...")

        await shutdown_vector_store()
        await shutdown_database()

        logger.info("Application shutdown completed successfully.")