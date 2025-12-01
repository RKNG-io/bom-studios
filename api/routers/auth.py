"""Authentication routes for magic link login."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from database import get_session
from models.db import Client
from services.auth import (
    create_access_token,
    create_magic_link_token,
    verify_magic_link_token,
)

router = APIRouter()
settings = get_settings()

Session = Annotated[AsyncSession, Depends(get_session)]


class MagicLinkRequest(BaseModel):
    email: EmailStr


class MagicLinkResponse(BaseModel):
    message: str
    # In dev mode, we include the token for testing
    token: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    client_id: str
    client_name: str


@router.post("/magic-link", response_model=MagicLinkResponse)
async def send_magic_link(
    session: Session,
    request: MagicLinkRequest,
):
    """
    Send a magic link to the client's email.

    In production, this would send an email via Resend.
    In dev mode, it returns the token directly for testing.
    """
    # Check if client exists
    stmt = select(Client).where(Client.email == request.email)
    result = await session.execute(stmt)
    client = result.scalar_one_or_none()

    if not client:
        # Don't reveal whether email exists or not
        # But still return success to prevent email enumeration
        return MagicLinkResponse(
            message="If an account exists with this email, a magic link has been sent.",
            token=None,
        )

    # Generate magic link token
    token = create_magic_link_token(request.email)

    # In production: send email via Resend
    # For now, we'll include the token in dev mode for testing
    if settings.debug:
        return MagicLinkResponse(
            message="Magic link generated (dev mode - token included)",
            token=token,
        )

    # TODO: Send email via Resend
    # await send_magic_link_email(request.email, token)

    return MagicLinkResponse(
        message="If an account exists with this email, a magic link has been sent.",
        token=None,
    )


@router.get("/verify", response_model=TokenResponse)
async def verify_magic_link(
    session: Session,
    token: str = Query(..., description="Magic link token from email"),
):
    """
    Verify a magic link token and return an access token.

    This is the endpoint the magic link URL points to.
    """
    # Verify the magic link token
    email = verify_magic_link_token(token)
    if not email:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired magic link",
        )

    # Get the client
    stmt = select(Client).where(Client.email == email)
    result = await session.execute(stmt)
    client = result.scalar_one_or_none()

    if not client:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired magic link",
        )

    # Create access token
    access_token = create_access_token(client.id, client.email)

    return TokenResponse(
        access_token=access_token,
        client_id=client.id,
        client_name=client.name,
    )


@router.get("/me")
async def get_current_client(
    session: Session,
    # In a real app, this would come from the middleware
    # For now, accept client_id as a query param for testing
    client_id: str = Query(..., description="Client ID from token"),
):
    """Get the current authenticated client's info."""
    stmt = select(Client).where(Client.id == client_id)
    result = await session.execute(stmt)
    client = result.scalar_one_or_none()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return {
        "id": client.id,
        "name": client.name,
        "email": client.email,
        "package": client.package,
    }
