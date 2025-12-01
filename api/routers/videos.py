from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_session
from models.db import Project, Video
from models.schemas import (
    VideoApproval,
    VideoCreate,
    VideoResponse,
    VideoUpdate,
    VideoWithAssets,
)

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_session)]


@router.get("", response_model=list[VideoResponse])
async def list_videos(
    session: Session,
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """List videos with optional filters."""
    stmt = select(Video)

    if project_id:
        stmt = stmt.where(Video.project_id == project_id)
    if status:
        stmt = stmt.where(Video.status == status)

    stmt = stmt.offset(skip).limit(limit).order_by(Video.created_at.desc())
    result = await session.execute(stmt)
    return result.scalars().all()


@router.post("", response_model=VideoResponse, status_code=201)
async def create_video(
    session: Session,
    video_in: VideoCreate,
):
    """Create a new video record."""
    # Verify project exists
    stmt = select(Project).where(Project.id == video_in.project_id)
    result = await session.execute(stmt)
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Project not found")

    video = Video(**video_in.model_dump())
    session.add(video)
    await session.flush()
    await session.refresh(video)
    return video


@router.get("/{video_id}", response_model=VideoWithAssets)
async def get_video(
    session: Session,
    video_id: str,
):
    """Get a video by ID with its assets."""
    stmt = (
        select(Video).where(Video.id == video_id).options(selectinload(Video.assets))
    )
    result = await session.execute(stmt)
    video = result.scalar_one_or_none()

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    return video


@router.patch("/{video_id}", response_model=VideoResponse)
async def update_video(
    session: Session,
    video_id: str,
    video_in: VideoUpdate,
):
    """Update a video."""
    stmt = select(Video).where(Video.id == video_id)
    result = await session.execute(stmt)
    video = result.scalar_one_or_none()

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    update_data = video_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(video, field, value)

    await session.flush()
    await session.refresh(video)
    return video


@router.post("/{video_id}/approve", response_model=VideoResponse)
async def approve_video(
    session: Session,
    video_id: str,
    approval: VideoApproval,
):
    """Client approval/rejection of a video."""
    stmt = select(Video).where(Video.id == video_id)
    result = await session.execute(stmt)
    video = result.scalar_one_or_none()

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    if video.status not in ("draft", "review"):
        raise HTTPException(
            status_code=400,
            detail=f"Video cannot be approved from status '{video.status}'",
        )

    if approval.approved:
        video.status = "approved"
        video.approved_at = datetime.utcnow()
    else:
        video.status = "draft"  # Back to draft for revision

    if approval.note:
        video.approval_note = approval.note

    await session.flush()
    await session.refresh(video)
    return video


@router.post("/{video_id}/reject", response_model=VideoResponse)
async def reject_video(
    session: Session,
    video_id: str,
    approval: VideoApproval,
):
    """Client rejection of a video with note."""
    stmt = select(Video).where(Video.id == video_id)
    result = await session.execute(stmt)
    video = result.scalar_one_or_none()

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    video.status = "draft"
    if approval.note:
        video.approval_note = approval.note

    await session.flush()
    await session.refresh(video)
    return video


@router.delete("/{video_id}", status_code=204)
async def delete_video(
    session: Session,
    video_id: str,
):
    """Delete a video and its assets."""
    stmt = select(Video).where(Video.id == video_id)
    result = await session.execute(stmt)
    video = result.scalar_one_or_none()

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    await session.delete(video)
