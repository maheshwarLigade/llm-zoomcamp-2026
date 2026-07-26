"""
Application Configuration

Centralized application configuration using Pydantic Settings.

Features
--------
- Environment variable support
- .env file support
- Type-safe configuration
- Validation
- Nested configuration
- Cached singleton instance

Author
------
Tech Knowledge Navigator
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic import computed_field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    ###########################################################################
    # Application
    ###########################################################################

    APP_NAME: str = "Tech Knowledge Navigator"

    APP_VERSION: str = "1.0.0"

    ENVIRONMENT: Literal[
        "development",
        "testing",
        "staging",
        "production",
    ] = "development"

    DEBUG: bool = True

    API_PREFIX: str = "/api/v1"

    SECRET_KEY: str = Field(
        ...,
        description="Application secret key.",
    )

    ###########################################################################
    # Server
    ###########################################################################

    HOST: str = "0.0.0.0"

    PORT: int = 8000

    WORKERS: int = 4

    ###########################################################################
    # Database
    ###########################################################################

    POSTGRES_HOST: str = "localhost"

    POSTGRES_PORT: int = 5432

    POSTGRES_DB: str = "rag"

    POSTGRES_USER: str = "postgres"

    POSTGRES_PASSWORD: str = "postgres"

    ###########################################################################
    # OpenSearch
    ###########################################################################

    OPENSEARCH_HOST: str = "localhost"

    OPENSEARCH_PORT: int = 9200

    OPENSEARCH_USERNAME: str = "admin"

    OPENSEARCH_PASSWORD: str = "admin"

    OPENSEARCH_INDEX: str = "knowledge"

    ###########################################################################
    # Qdrant
    ###########################################################################

    QDRANT_HOST: str = "localhost"

    QDRANT_PORT: int = 6333

    QDRANT_COLLECTION: str = "knowledge"

    ###########################################################################
    # Embeddings
    ###########################################################################

    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    EMBEDDING_DIMENSION: int = 384

    ###########################################################################
    # Re-ranking
    ###########################################################################

    RERANKER_MODEL: str = "BAAI/bge-reranker-base"

    ###########################################################################
    # LLM
    ###########################################################################

    LLM_PROVIDER: Literal[
        "openai",
        "ollama",
        "groq",
    ] = "openai"

    OPENAI_API_KEY: str | None = None

    OPENAI_MODEL: str = "gpt-4.1-mini"

    GROQ_API_KEY: str | None = None

    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    OLLAMA_BASE_URL: str = "http://localhost:11434"

    OLLAMA_MODEL: str = "llama3.2"

    ###########################################################################
    # Retrieval
    ###########################################################################

    TOP_K: int = 5

    ENABLE_HYBRID_SEARCH: bool = True

    ENABLE_RERANKING: bool = True

    ENABLE_QUERY_REWRITE: bool = True

    ###########################################################################
    # Chunking
    ###########################################################################

    CHUNK_SIZE: int = 512

    CHUNK_OVERLAP: int = 64

    ###########################################################################
    # Monitoring
    ###########################################################################

    ENABLE_METRICS: bool = True

    METRICS_PATH: str = "/metrics"

    ###########################################################################
    # Logging
    ###########################################################################

    LOG_LEVEL: str = "INFO"

    LOG_FORMAT: str = (
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    ###########################################################################
    # CORS
    ###########################################################################

    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8501",
    ]

    ###########################################################################
    # JWT
    ###########################################################################

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    ALGORITHM: str = "HS256"

    ###########################################################################
    # Computed Properties
    ###########################################################################

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    @computed_field
    @property
    def opensearch_url(self) -> str:
        return (
            f"http://{self.OPENSEARCH_HOST}:"
            f"{self.OPENSEARCH_PORT}"
        )

    @computed_field
    @property
    def qdrant_url(self) -> str:
        return (
            f"http://{self.QDRANT_HOST}:"
            f"{self.QDRANT_PORT}"
        )


@lru_cache
def get_settings() -> Settings:
    """
    Returns cached application settings.

    The configuration is loaded only once during the
    application lifecycle.
    """
    return Settings()


settings = get_settings()