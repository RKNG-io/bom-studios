"""Authentication middleware for JWT token verification."""

from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from services.auth import verify_access_token

security = HTTPBearer(auto_error=False)


async def get_current_client(
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(security)],
) -> dict:
    """
    Dependency that extracts and verifies the JWT token from the Authorization header.

    Returns the client info if valid, raises 401 if not.

    Usage:
        @router.get("/protected")
        async def protected_route(client: dict = Depends(get_current_client)):
            return {"client_id": client["client_id"]}
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = verify_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


async def get_optional_client(
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(security)],
) -> Optional[dict]:
    """
    Dependency that optionally extracts the JWT token.

    Returns the client info if valid token present, None otherwise.
    Does not raise an error for missing/invalid tokens.

    Usage:
        @router.get("/public-or-private")
        async def route(client: Optional[dict] = Depends(get_optional_client)):
            if client:
                return {"message": "Hello, authenticated user!"}
            return {"message": "Hello, anonymous user!"}
    """
    if not credentials:
        return None

    return verify_access_token(credentials.credentials)
