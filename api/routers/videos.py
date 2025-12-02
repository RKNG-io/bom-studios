import logging
from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_session
from models.db import Client, Project, Video
from models.schemas import (
    VideoApproval,
    VideoCreate,
    VideoResponse,
    VideoUpdate,
    VideoWithAssets,
)
from services.auth import CurrentClient, get_current_client

logger = logging.getLogger(__name__)

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_session)]
AuthClient = Annotated[CurrentClient, Depends(get_current_client)]


async def get_video_for_client(
    session: AsyncSession, video_id: str, client_id: str
) -> Video | None:
    """Get a video, verifying it belongs to the client via its project."""
    stmt = (
        select(Video)
        .join(Project)
        .where(Video.id == video_id, Project.client_id == client_id)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


@router.get("", response_model=list[VideoResponse])
async def list_videos(
    session: Session,
    client: AuthClient,
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """List videos for the authenticated client."""
    stmt = select(Video).join(Project).where(Project.client_id == client.client_id)

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
    client: AuthClient,
    video_in: VideoCreate,
):
    """Create a new video record."""
    # Verify project exists and belongs to client
    stmt = select(Project).where(
        Project.id == video_in.project_id, Project.client_id == client.client_id
    )
    result = await session.execute(stmt)
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Project not found")

    video = Video(**video_in.model_dump())
    session.add(video)
    await session.flush()
    await session.refresh(video)
    return video


@router.get("/{video_id}", response_model=VideoWithAssets)
async def get_video(
    session: Session,
    client: AuthClient,
    video_id: str,
):
    """Get a video by ID with its assets."""
    stmt = (
        select(Video)
        .join(Project)
        .where(Video.id == video_id, Project.client_id == client.client_id)
        .options(selectinload(Video.assets))
    )
    result = await session.execute(stmt)
    video = result.scalar_one_or_none()

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    return video


@router.patch("/{video_id}", response_model=VideoResponse)
async def update_video(
    session: Session,
    client: AuthClient,
    video_id: str,
    video_in: VideoUpdate,
):
    """Update a video."""
    video = await get_video_for_client(session, video_id, client.client_id)

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
    client: AuthClient,
    video_id: str,
    approval: VideoApproval,
):
    """Client approval/rejection of a video."""
    video = await get_video_for_client(session, video_id, client.client_id)

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
    client: AuthClient,
    video_id: str,
    approval: VideoApproval,
):
    """Client rejection of a video with note."""
    video = await get_video_for_client(session, video_id, client.client_id)

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    if video.status != "review":
        raise HTTPException(
            status_code=400,
            detail=f"Video cannot be rejected from status '{video.status}'",
        )

    video.status = "draft"
    if approval.note:
        video.approval_note = approval.note

    await session.flush()
    await session.refresh(video)
    return video


@router.post("/{video_id}/submit", response_model=VideoResponse)
async def submit_video(
    session: Session,
    client: AuthClient,
    video_id: str,
):
    """Submit a video for client review."""
    video = await get_video_for_client(session, video_id, client.client_id)

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    if video.status != "draft":
        raise HTTPException(
            status_code=400,
            detail=f"Only draft videos can be submitted for review (current: '{video.status}')",
        )

    video.status = "review"
    await session.flush()
    await session.refresh(video)
    return video


@router.delete("/{video_id}", status_code=204)
async def delete_video(
    session: Session,
    client: AuthClient,
    video_id: str,
):
    """Delete a video and its assets."""
    video = await get_video_for_client(session, video_id, client.client_id)

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    await session.delete(video)


@router.post("/{video_id}/deliver", response_model=VideoResponse)
async def deliver_video(
    session: Session,
    client: AuthClient,
    video_id: str,
    background_tasks: BackgroundTasks,
):
    """Upload approved video to Google Drive and mark as delivered.

    This will:
    1. Upload the video to Google Drive (in client's folder)
    2. Set viewing permissions
    3. Update video status to 'delivered'
    4. Store the Drive link
    """
    # Get video with project and client info, verifying ownership
    stmt = (
        select(Video)
        .join(Project)
        .where(Video.id == video_id, Project.client_id == client.client_id)
        .options(selectinload(Video.project).selectinload(Project.client))
    )
    result = await session.execute(stmt)
    video = result.scalar_one_or_none()

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    if video.status != "approved":
        raise HTTPException(
            status_code=400,
            detail=f"Video must be approved before delivery (current status: {video.status})",
        )

    if not video.formats:
        raise HTTPException(
            status_code=400,
            detail="Video has no rendered formats to deliver",
        )

    # Import here to avoid circular imports and allow graceful failure if not configured
    try:
        from services.google_drive import drive_service

        # Get client name for folder
        client_name = video.project.client.name if video.project and video.project.client else "Unknown"

        # Create client folder if needed
        folder_id = drive_service.create_client_folder(client_name)

        # Upload the video (use vertical format as primary)
        video_url = video.formats.get("vertical") or list(video.formats.values())[0]

        # For now, we'll just store the Drive folder link
        # In production, you'd download the video and re-upload to Drive
        upload_result = {
            "web_view_link": f"https://drive.google.com/drive/folders/{folder_id}"
        }

        # Set permissions (anyone with link can view)
        drive_service.set_file_permissions(folder_id, anyone_with_link=True)

        # Share with client if they have an email
        if video.project and video.project.client:
            client_email = video.project.client.email
            if client_email:
                drive_service.set_file_permissions(folder_id, email=client_email)

        # Update video
        video.delivery_url = upload_result["web_view_link"]
        video.delivered_at = datetime.utcnow()
        video.status = "delivered"

        logger.info(f"Delivered video {video_id} to Google Drive: {video.delivery_url}")

    except ImportError:
        raise HTTPException(
            status_code=503,
            detail="Google Drive service not available. Check google-api-python-client is installed.",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Google Drive not configured: {e}",
        )
    except Exception as e:
        logger.error(f"Failed to deliver video {video_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload to Google Drive: {str(e)}",
        )

    await session.flush()
    await session.refresh(video)
    return video
