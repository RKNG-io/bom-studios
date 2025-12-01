from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models.db import Client
from models.schemas import ClientCreate, ClientResponse, ClientUpdate

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_session)]


@router.get("", response_model=list[ClientResponse])
async def list_clients(
    session: Session,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """List all clients with pagination."""
    stmt = select(Client).offset(skip).limit(limit).order_by(Client.created_at.desc())
    result = await session.execute(stmt)
    return result.scalars().all()


@router.post("", response_model=ClientResponse, status_code=201)
async def create_client(
    session: Session,
    client_in: ClientCreate,
):
    """Create a new client."""
    # Check for duplicate email
    stmt = select(Client).where(Client.email == client_in.email)
    result = await session.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail=f"Client with email '{client_in.email}' already exists",
        )

    client = Client(**client_in.model_dump())
    session.add(client)
    await session.flush()
    await session.refresh(client)
    return client


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    session: Session,
    client_id: str,
):
    """Get a client by ID."""
    stmt = select(Client).where(Client.id == client_id)
    result = await session.execute(stmt)
    client = result.scalar_one_or_none()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return client


@router.patch("/{client_id}", response_model=ClientResponse)
async def update_client(
    session: Session,
    client_id: str,
    client_in: ClientUpdate,
):
    """Update a client."""
    stmt = select(Client).where(Client.id == client_id)
    result = await session.execute(stmt)
    client = result.scalar_one_or_none()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Check for duplicate email if updating email
    if client_in.email and client_in.email != client.email:
        stmt = select(Client).where(Client.email == client_in.email)
        result = await session.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail=f"Client with email '{client_in.email}' already exists",
            )

    update_data = client_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(client, field, value)

    await session.flush()
    await session.refresh(client)
    return client


@router.delete("/{client_id}", status_code=204)
async def delete_client(
    session: Session,
    client_id: str,
):
    """Delete a client and all their projects."""
    stmt = select(Client).where(Client.id == client_id)
    result = await session.execute(stmt)
    client = result.scalar_one_or_none()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    await session.delete(client)
