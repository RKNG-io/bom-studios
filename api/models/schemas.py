from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------- Client Schemas ----------
class ClientCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    package: str = Field(default="kickstart", pattern="^(kickstart|growth|pro)$")
    brand_kit: Optional[dict] = None


class ClientUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    package: Optional[str] = Field(None, pattern="^(kickstart|growth|pro)$")
    brand_kit: Optional[dict] = None


class ClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    email: str
    package: str
    brand_kit: Optional[dict]
    created_at: datetime
    updated_at: datetime


# ---------- Project Schemas ----------
class ProjectCreate(BaseModel):
    client_id: str
    name: str = Field(..., min_length=1, max_length=255)


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    status: Optional[str] = Field(
        None, pattern="^(draft|in_progress|review|approved|delivered)$"
    )


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    client_id: str
    name: str
    status: str
    created_at: datetime
    updated_at: datetime


class ProjectWithVideos(ProjectResponse):
    videos: list["VideoResponse"] = []


# ---------- Video Schemas ----------
class VideoCreate(BaseModel):
    project_id: str
    title: str = Field(..., min_length=1, max_length=255)
    script: Optional[dict] = None


class VideoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    script: Optional[dict] = None
    status: Optional[str] = Field(
        None,
        pattern="^(scripting|generating|rendering|draft|approved|delivered)$",
    )
    formats: Optional[dict] = None
    cost_cents: Optional[int] = Field(None, ge=0)


class VideoApproval(BaseModel):
    approved: bool
    note: Optional[str] = None


class VideoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    project_id: str
    title: str
    script: Optional[dict]
    status: str
    formats: Optional[dict]
    cost_cents: int
    approval_note: Optional[str]
    approved_at: Optional[datetime]
    delivery_url: Optional[str]
    delivered_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class VideoWithAssets(VideoResponse):
    assets: list["AssetResponse"] = []


# ---------- Asset Schemas ----------
class AssetCreate(BaseModel):
    video_id: str
    type: str = Field(..., pattern="^(image|audio|music|clip)$")
    url: str
    meta: Optional[dict] = None


class AssetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    video_id: str
    type: str
    url: str
    meta: Optional[dict]
    created_at: datetime


# ---------- API Usage Schemas ----------
class APIUsageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    provider: str
    action: str
    project_id: Optional[str]
    cost_cents: int
    created_at: datetime


# Rebuild forward references
ProjectWithVideos.model_rebuild()
VideoWithAssets.model_rebuild()
