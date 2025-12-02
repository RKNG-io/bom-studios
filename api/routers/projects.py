from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_session
from models.db import Client, Project
from models.schemas import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
    ProjectWithVideos,
)
from services.auth import CurrentClient, get_current_client

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_session)]
AuthClient = Annotated[CurrentClient, Depends(get_current_client)]


@router.get("", response_model=list[ProjectResponse])
async def list_projects(
    session: Session,
    client: AuthClient,
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """List projects for the authenticated client."""
    stmt = select(Project).where(Project.client_id == client.client_id)

    if status:
        stmt = stmt.where(Project.status == status)

    stmt = stmt.offset(skip).limit(limit).order_by(Project.created_at.desc())
    result = await session.execute(stmt)
    return result.scalars().all()


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(
    session: Session,
    client: AuthClient,
    project_in: ProjectCreate,
):
    """Create a new project for the authenticated client."""
    # Ensure client can only create projects for themselves
    if project_in.client_id != client.client_id:
        raise HTTPException(status_code=403, detail="Cannot create project for another client")

    project = Project(**project_in.model_dump())
    session.add(project)
    await session.flush()
    await session.refresh(project)
    return project


@router.get("/{project_id}", response_model=ProjectWithVideos)
async def get_project(
    session: Session,
    client: AuthClient,
    project_id: str,
):
    """Get a project by ID with its videos."""
    stmt = (
        select(Project)
        .where(Project.id == project_id, Project.client_id == client.client_id)
        .options(selectinload(Project.videos))
    )
    result = await session.execute(stmt)
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    session: Session,
    client: AuthClient,
    project_id: str,
    project_in: ProjectUpdate,
):
    """Update a project."""
    stmt = select(Project).where(
        Project.id == project_id, Project.client_id == client.client_id
    )
    result = await session.execute(stmt)
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = project_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    await session.flush()
    await session.refresh(project)
    return project


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    session: Session,
    client: AuthClient,
    project_id: str,
):
    """Delete a project and all its videos."""
    stmt = select(Project).where(
        Project.id == project_id, Project.client_id == client.client_id
    )
    result = await session.execute(stmt)
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    await session.delete(project)
