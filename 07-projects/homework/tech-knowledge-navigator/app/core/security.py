"""
Security Utilities

Centralized security implementation.

Features
--------
- JWT Authentication
- Password Hashing
- API Key Validation
- RBAC
- Password Validation
- Secret Generation

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations

import re
import secrets
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any

import jwt
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Security
from fastapi.security import APIKeyHeader
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.core.config import settings

###############################################################################
# Password Hashing
###############################################################################

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

###############################################################################
# OAuth2
###############################################################################

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)

###############################################################################
# API Key
###############################################################################

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
)

###############################################################################
# Password Utilities
###############################################################################


def hash_password(password: str) -> str:
    """
    Hash password using bcrypt.
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify password.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


###############################################################################
# JWT
###############################################################################


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    """
    Creates JWT token.
    """

    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    )

    payload = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }

    if additional_claims:
        payload.update(additional_claims)

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode JWT token.
    """

    try:

        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired.",
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token.",
        )


###############################################################################
# Authentication Dependency
###############################################################################


def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    """
    Returns authenticated user.
    """

    payload = decode_token(token)

    return {
        "id": payload.get("sub"),
        "username": payload.get("username"),
        "roles": payload.get("roles", []),
    }


###############################################################################
# API Key Authentication
###############################################################################


def validate_api_key(
    api_key: str | None = Security(api_key_header),
):
    """
    Validate API key.
    """

    if api_key is None:
        raise HTTPException(
            status_code=401,
            detail="Missing API Key.",
        )

    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key.",
        )

    return api_key


###############################################################################
# RBAC
###############################################################################


def require_role(role: str):
    """
    Dependency factory.

    Example

    Depends(require_role("ADMIN"))
    """

    def checker(user=Depends(get_current_user)):

        if role not in user["roles"]:

            raise HTTPException(
                status_code=403,
                detail="Access denied.",
            )

        return user

    return checker


###############################################################################
# Password Validation
###############################################################################


def validate_password_strength(
    password: str,
) -> tuple[bool, list[str]]:
    """
    Password validation.
    """

    errors = []

    if len(password) < 8:
        errors.append(
            "Minimum length is 8."
        )

    if not re.search(r"[A-Z]", password):
        errors.append(
            "Missing uppercase letter."
        )

    if not re.search(r"[a-z]", password):
        errors.append(
            "Missing lowercase letter."
        )

    if not re.search(r"\d", password):
        errors.append(
            "Missing digit."
        )

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append(
            "Missing special character."
        )

    return len(errors) == 0, errors


###############################################################################
# Secret Generator
###############################################################################


def generate_secret(
    length: int = 64,
) -> str:
    """
    Generate secure random secret.
    """

    return secrets.token_urlsafe(length)


###############################################################################
# Token Helper
###############################################################################


def create_refresh_token(
    subject: str,
) -> str:
    """
    Creates refresh token.
    """

    return create_access_token(
        subject=subject,
        expires_delta=timedelta(days=30),
    )


###############################################################################
# Authorization Helpers
###############################################################################


def is_admin(user: dict) -> bool:
    return "ADMIN" in user.get("roles", [])


def has_role(
    user: dict,
    role: str,
) -> bool:
    return role in user.get("roles", [])


###############################################################################
# Constants
###############################################################################

DEFAULT_USER_ROLE = "USER"

DEFAULT_ADMIN_ROLE = "ADMIN"