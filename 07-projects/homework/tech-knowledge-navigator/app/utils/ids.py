"""
ID Generation Utilities

Centralized ID generation utilities used across
the RAG application.

Provides:
- UUID generation
- Entity-specific identifiers
- Trace identifiers
- Human-readable IDs

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations

import time
import uuid

from datetime import datetime
from datetime import timezone



###############################################################################
# UUID Generation
###############################################################################


def generate_uuid() -> str:
    """
    Generate standard UUID4.

    Used for:
    - database entities
    - conversations
    - feedback
    - evaluations
    """

    return str(uuid.uuid4())



def generate_uuid_object() -> uuid.UUID:
    """
    Generate UUID object.

    Useful when working with:
    - SQLAlchemy UUID columns
    - Pydantic UUID fields
    """

    return uuid.uuid4()



###############################################################################
# Request / Trace IDs
###############################################################################


def generate_request_id() -> str:
    """
    Generate request correlation ID.

    Example:
        req_a8f92b7c3d1e

    Used for:
    - API logs
    - distributed tracing
    - debugging
    """

    return (
        "req_"
        + uuid.uuid4().hex[:12]
    )



def generate_trace_id() -> str:
    """
    Generate distributed tracing ID.

    Used for:
    - LLM calls
    - retrieval pipeline tracing
    - monitoring
    """

    return (
        "trace_"
        + uuid.uuid4().hex[:16]
    )



###############################################################################
# Entity IDs
###############################################################################


def generate_document_id() -> str:
    """
    Generate document identifier.
    """

    return (
        "doc_"
        + uuid.uuid4().hex
    )



def generate_chunk_id() -> str:
    """
    Generate document chunk identifier.
    """

    return (
        "chunk_"
        + uuid.uuid4().hex
    )



def generate_conversation_id() -> str:
    """
    Generate chat conversation identifier.
    """

    return (
        "conv_"
        + uuid.uuid4().hex
    )



def generate_message_id() -> str:
    """
    Generate chat message identifier.
    """

    return (
        "msg_"
        + uuid.uuid4().hex
    )



def generate_ingestion_id() -> str:
    """
    Generate ingestion job identifier.
    """

    return (
        "ing_"
        + uuid.uuid4().hex
    )



def generate_evaluation_id() -> str:
    """
    Generate evaluation run identifier.
    """

    return (
        "eval_"
        + uuid.uuid4().hex
    )



def generate_feedback_id() -> str:
    """
    Generate feedback identifier.
    """

    return (
        "feedback_"
        + uuid.uuid4().hex
    )



###############################################################################
# Short IDs
###############################################################################


def generate_short_id(
    prefix: str = "",
    length: int = 8,
) -> str:
    """
    Generate short readable identifier.

    Example:

        search_92ab31cd

    """

    identifier = uuid.uuid4().hex[:length]

    if prefix:
        return f"{prefix}_{identifier}"

    return identifier



###############################################################################
# Time Based IDs
###############################################################################


def generate_timestamp_id(
    prefix: str = "",
) -> str:
    """
    Generate time-based identifier.

    Useful for:
    - logs
    - audit records
    - exported files
    """

    timestamp = datetime.now(
        timezone.utc
    ).strftime(
        "%Y%m%d%H%M%S"
    )

    random_part = uuid.uuid4().hex[:6]

    identifier = (
        f"{timestamp}_{random_part}"
    )

    if prefix:
        return (
            f"{prefix}_{identifier}"
        )

    return identifier



###############################################################################
# Numeric IDs
###############################################################################


def generate_epoch_id() -> int:
    """
    Generate epoch based ID.

    Example:

    1721987654321
    """

    return int(
        time.time() * 1000
    )



###############################################################################
# Validation Utilities
###############################################################################


def is_valid_uuid(
    value: str,
) -> bool:
    """
    Validate UUID string.
    """

    try:

        uuid.UUID(value)

        return True

    except ValueError:

        return False



###############################################################################
# Namespace IDs
###############################################################################


def generate_namespace_id(
    namespace: str,
    value: str,
) -> str:
    """
    Generate deterministic UUID.

    Same namespace + value
    always produces same ID.

    Useful for:
    - duplicate document detection
    - external references
    """

    namespace_uuid = uuid.uuid5(
        uuid.NAMESPACE_DNS,
        namespace,
    )

    return str(
        uuid.uuid5(
            namespace_uuid,
            value,
        )
    )