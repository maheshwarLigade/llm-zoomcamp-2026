"""
Application Constants

Contains immutable constants used throughout the application.

IMPORTANT

Only application constants belong here.

Configurable values belong in config.py

Author
------
Tech Knowledge Navigator
"""

###############################################################################
# Application
###############################################################################

APP_NAME = "Tech Knowledge Navigator"

APP_DESCRIPTION = (
    "Production-grade Retrieval-Augmented Generation (RAG) "
    "platform for technical knowledge search."
)

API_VERSION = "v1"

API_PREFIX = "/api/v1"

###############################################################################
# API Headers
###############################################################################

HEADER_REQUEST_ID = "X-Request-ID"

HEADER_CORRELATION_ID = "X-Correlation-ID"

HEADER_API_KEY = "X-API-Key"

HEADER_USER_AGENT = "User-Agent"

###############################################################################
# Content Types
###############################################################################

APPLICATION_JSON = "application/json"

TEXT_PLAIN = "text/plain"

TEXT_HTML = "text/html"

APPLICATION_PDF = "application/pdf"

MULTIPART_FORM_DATA = "multipart/form-data"

###############################################################################
# Search Types
###############################################################################

SEARCH_KEYWORD = "keyword"

SEARCH_VECTOR = "vector"

SEARCH_HYBRID = "hybrid"

###############################################################################
# Retrieval Defaults
###############################################################################

DEFAULT_TOP_K = 5

MAX_TOP_K = 50

MIN_TOP_K = 1

DEFAULT_SCORE_THRESHOLD = 0.70

###############################################################################
# Chunking
###############################################################################

DEFAULT_CHUNK_SIZE = 512

DEFAULT_CHUNK_OVERLAP = 64

MAX_CHUNK_SIZE = 4096

###############################################################################
# Embedding Models
###############################################################################

BGE_SMALL = "BAAI/bge-small-en-v1.5"

BGE_BASE = "BAAI/bge-base-en-v1.5"

BGE_LARGE = "BAAI/bge-large-en-v1.5"

###############################################################################
# Re-ranking Models
###############################################################################

BGE_RERANKER_BASE = "BAAI/bge-reranker-base"

BGE_RERANKER_LARGE = "BAAI/bge-reranker-large"

###############################################################################
# Supported LLM Providers
###############################################################################

OPENAI = "openai"

OLLAMA = "ollama"

GROQ = "groq"

###############################################################################
# Chat Roles
###############################################################################

SYSTEM = "system"

USER = "user"

ASSISTANT = "assistant"

TOOL = "tool"

###############################################################################
# Document Types
###############################################################################

PDF = "pdf"

TEXT = "text"

MARKDOWN = "markdown"

HTML = "html"

JSON = "json"

CSV = "csv"

DOCX = "docx"

###############################################################################
# Database Tables
###############################################################################

TABLE_DOCUMENTS = "documents"

TABLE_DOCUMENT_CHUNKS = "document_chunks"

TABLE_CHAT_HISTORY = "chat_history"

TABLE_FEEDBACK = "feedback"

TABLE_EVALUATIONS = "evaluations"

TABLE_INGESTION_JOBS = "ingestion_jobs"

###############################################################################
# Vector Collections
###############################################################################

DEFAULT_QDRANT_COLLECTION = "knowledge"

###############################################################################
# OpenSearch Index
###############################################################################

DEFAULT_OPENSEARCH_INDEX = "knowledge"

###############################################################################
# Cache Keys
###############################################################################

CACHE_CHAT = "chat"

CACHE_EMBEDDINGS = "embeddings"

CACHE_SEARCH = "search"

CACHE_DOCUMENT = "document"

###############################################################################
# Pagination
###############################################################################

DEFAULT_PAGE = 1

DEFAULT_PAGE_SIZE = 20

MAX_PAGE_SIZE = 100

###############################################################################
# Job Status
###############################################################################

STATUS_PENDING = "PENDING"

STATUS_RUNNING = "RUNNING"

STATUS_COMPLETED = "COMPLETED"

STATUS_FAILED = "FAILED"

STATUS_CANCELLED = "CANCELLED"

###############################################################################
# Feedback
###############################################################################

POSITIVE = "positive"

NEGATIVE = "negative"

NEUTRAL = "neutral"

###############################################################################
# Monitoring
###############################################################################

PROMETHEUS_METRICS_PATH = "/metrics"

HEALTH_ENDPOINT = "/health"

READY_ENDPOINT = "/ready"

LIVE_ENDPOINT = "/live"

###############################################################################
# Metrics
###############################################################################

METRIC_REQUEST_COUNT = "rag_requests_total"

METRIC_REQUEST_LATENCY = "rag_request_duration_seconds"

METRIC_RETRIEVAL_LATENCY = "rag_retrieval_duration_seconds"

METRIC_LLM_LATENCY = "rag_llm_duration_seconds"

METRIC_TOKEN_USAGE = "rag_tokens_total"

METRIC_CACHE_HITS = "rag_cache_hits_total"

METRIC_CACHE_MISSES = "rag_cache_misses_total"

###############################################################################
# Error Codes
###############################################################################

ERR_DOCUMENT_NOT_FOUND = "DOCUMENT_NOT_FOUND"

ERR_INDEX_NOT_FOUND = "INDEX_NOT_FOUND"

ERR_INVALID_QUERY = "INVALID_QUERY"

ERR_EMBEDDING_FAILURE = "EMBEDDING_FAILURE"

ERR_RETRIEVAL_FAILURE = "RETRIEVAL_FAILURE"

ERR_LLM_FAILURE = "LLM_FAILURE"

ERR_INTERNAL_SERVER = "INTERNAL_SERVER_ERROR"

###############################################################################
# Logging
###############################################################################

LOGGER_NAME = "rag"

###############################################################################
# Timeouts
###############################################################################

DEFAULT_HTTP_TIMEOUT = 30

DEFAULT_LLM_TIMEOUT = 120

DEFAULT_DATABASE_TIMEOUT = 30

###############################################################################
# File Upload
###############################################################################

MAX_FILE_SIZE_MB = 50

SUPPORTED_FILE_TYPES = (
    ".pdf",
    ".txt",
    ".md",
    ".docx",
    ".html",
    ".json",
    ".csv",
)

###############################################################################
# Evaluation Metrics
###############################################################################

METRIC_PRECISION = "precision"

METRIC_RECALL = "recall"

METRIC_MRR = "mrr"

METRIC_NDCG = "ndcg"

METRIC_FAITHFULNESS = "faithfulness"

METRIC_CONTEXT_RECALL = "context_recall"

METRIC_CONTEXT_PRECISION = "context_precision"

METRIC_ANSWER_RELEVANCY = "answer_relevancy"

###############################################################################
# Default Prompt Names
###############################################################################

DEFAULT_CHAT_PROMPT = "chat"

QUERY_REWRITE_PROMPT = "query_rewrite"

SUMMARY_PROMPT = "summary"

###############################################################################
# Application Tags
###############################################################################

TAG_CHAT = "Chat"

TAG_SEARCH = "Search"

TAG_DOCUMENTS = "Documents"

TAG_INGESTION = "Ingestion"

TAG_EVALUATION = "Evaluation"

TAG_FEEDBACK = "Feedback"

TAG_MONITORING = "Monitoring"

TAG_ADMIN = "Administration"

TAG_HEALTH = "Health"