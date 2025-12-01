"""Authentication service for magic link and JWT token handling."""

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

from config import get_settings

settings = get_settings()


def create_magic_link_token(email: str) -> str:
    """Create a short-lived token for magic link authentication."""
    expire = datetime.utcnow() + timedelta(minutes=settings.magic_link_expire_minutes)
    payload = {
        "sub": email,
        "type": "magic_link",
        "exp": expire,
    }
    return jwt.encode(payload, settings.magic_link_secret, algorithm=settings.jwt_algorithm)


def verify_magic_link_token(token: str) -> Optional[str]:
    """
    Verify a magic link token and return the email if valid.
    Returns None if token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.magic_link_secret,
            algorithms=[settings.jwt_algorithm],
        )
        if payload.get("type") != "magic_link":
            return None
        return payload.get("sub")
    except JWTError:
        return None


def create_access_token(client_id: str, email: str) -> str:
    """Create a long-lived JWT access token for authenticated sessions."""
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": client_id,
        "email": email,
        "type": "access",
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def verify_access_token(token: str) -> Optional[dict]:
    """
    Verify an access token and return the payload if valid.
    Returns None if token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        if payload.get("type") != "access":
            return None
        return {
            "client_id": payload.get("sub"),
            "email": payload.get("email"),
        }
    except JWTError:
        return None
