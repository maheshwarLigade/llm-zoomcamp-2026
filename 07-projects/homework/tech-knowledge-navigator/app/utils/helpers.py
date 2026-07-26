"""
Common Helper Utilities

Reusable utility functions shared across the application.

This module must remain framework independent.

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import hashlib
import json
import os
import re

from datetime import datetime
from datetime import timezone

from pathlib import Path
from typing import Any

from uuid import UUID
from uuid import uuid4



###############################################################################
# UUID Utilities
###############################################################################


def generate_uuid() -> UUID:
    """
    Generate UUID4.

    Returns:
        UUID
    """

    return uuid4()



###############################################################################
# Date Time Utilities
###############################################################################


def utc_now() -> datetime:
    """
    Return current UTC datetime.
    """

    return datetime.now(
        timezone.utc
    )



def datetime_to_iso(
    value: datetime,
) -> str:
    """
    Convert datetime to ISO string.
    """

    return value.isoformat()



###############################################################################
# Hash Utilities
###############################################################################


def generate_hash(
    value: str,
    algorithm: str = "sha256",
) -> str:
    """
    Generate deterministic hash.

    Used for:
    - document fingerprinting
    - duplicate detection
    - cache keys
    """

    hash_function = hashlib.new(
        algorithm
    )

    hash_function.update(
        value.encode("utf-8")
    )

    return hash_function.hexdigest()



def generate_file_hash(
    file_path: str,
) -> str:
    """
    Generate hash of file content.
    """

    sha256 = hashlib.sha256()

    with open(
        file_path,
        "rb",
    ) as file:

        for chunk in iter(
            lambda: file.read(4096),
            b"",
        ):
            sha256.update(chunk)

    return sha256.hexdigest()



###############################################################################
# JSON Utilities
###############################################################################


def serialize_json(
    data: Any,
) -> str:
    """
    Convert object to JSON string.
    """

    return json.dumps(
        data,
        default=str,
        ensure_ascii=False,
    )



def deserialize_json(
    value: str,
) -> Any:
    """
    Convert JSON string to object.
    """

    return json.loads(
        value
    )



def is_valid_json(
    value: str,
) -> bool:
    """
    Check whether string is valid JSON.
    """

    try:

        json.loads(value)

        return True

    except Exception:

        return False



###############################################################################
# Text Utilities
###############################################################################


def normalize_text(
    text: str,
) -> str:
    """
    Normalize text before indexing.

    Used during:
    - document ingestion
    - chunking
    - embeddings
    """

    text = text.strip()

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text



def clean_filename(
    filename: str,
) -> str:
    """
    Make filename safe.
    """

    filename = re.sub(
        r"[^a-zA-Z0-9._-]",
        "_",
        filename,
    )

    return filename.lower()



###############################################################################
# Token Utilities
###############################################################################


def estimate_tokens(
    text: str,
) -> int:
    """
    Approximate token count.

    Rule:
    ~4 characters = 1 token

    Used for:
    - prompt estimation
    - cost calculation
    """

    if not text:
        return 0

    return max(
        1,
        len(text) // 4,
    )



###############################################################################
# File Utilities
###############################################################################


def ensure_directory(
    path: str,
) -> Path:
    """
    Create directory if missing.
    """

    directory = Path(path)

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory



def read_file(
    file_path: str,
) -> str:
    """
    Read text file.
    """

    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as file:

        return file.read()



def write_file(
    file_path: str,
    content: str,
):
    """
    Write content to file.
    """

    path = Path(file_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(content)



###############################################################################
# Dictionary Utilities
###############################################################################


def get_nested_value(
    data: dict,
    keys: list[str],
    default=None,
):
    """
    Safely get nested dictionary value.

    Example:

    get_nested_value(
        payload,
        ["user","name"]
    )
    """

    current = data

    for key in keys:

        if not isinstance(
            current,
            dict,
        ):
            return default

        current = current.get(
            key
        )

        if current is None:
            return default

    return current



def merge_dicts(
    first: dict,
    second: dict,
) -> dict:
    """
    Merge dictionaries.
    """

    result = first.copy()

    result.update(
        second
    )

    return result



###############################################################################
# Pagination Utilities
###############################################################################


def calculate_offset(
    page: int,
    page_size: int,
) -> int:
    """
    Calculate database offset.
    """

    return (
        page - 1
    ) * page_size



def calculate_total_pages(
    total_items: int,
    page_size: int,
) -> int:
    """
    Calculate number of pages.
    """

    if total_items == 0:
        return 0

    return (
        total_items + page_size - 1
    ) // page_size



###############################################################################
# Environment Utilities
###############################################################################


def get_env(
    key: str,
    default: str | None = None,
) -> str | None:
    """
    Get environment variable.
    """

    return os.getenv(
        key,
        default,
    )



###############################################################################
# Masking Utilities
###############################################################################


def mask_secret(
    value: str,
    visible_chars: int = 4,
) -> str:
    """
    Hide sensitive information.

    Example:

    abcdefgh1234

    becomes

    ********1234
    """

    if not value:
        return value

    if len(value) <= visible_chars:
        return "*" * len(value)

    return (
        "*" *
        (
            len(value)
            -
            visible_chars
        )
        +
        value[-visible_chars:]
    )