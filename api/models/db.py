import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    package: Mapped[str] = mapped_column(String(50), default="kickstart")
    brand_kit: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    projects: Mapped[list["Project"]] = relationship(
        back_populates="client", cascade="all, delete-orphan"
    )


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    client_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("clients.id"), index=True
    )
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default="draft")
    # Status values: draft, in_progress, review, approved, delivered
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    client: Mapped["Client"] = relationship(back_populates="projects")
    videos: Mapped[list["Video"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id"), index=True
    )
    title: Mapped[str] = mapped_column(String(255))
    script: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    # Script format: {"hook": "...", "scenes": [...], "cta": "..."}
    status: Mapped[str] = mapped_column(String(50), default="scripting")
    # Status values: scripting, generating, rendering, draft, approved, delivered
    formats: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    # Formats: {"vertical": "url", "square": "url", "horizontal": "url"}
    cost_cents: Mapped[int] = mapped_column(default=0)
    approval_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    approved_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="videos")
    assets: Mapped[list["Asset"]] = relationship(
        back_populates="video", cascade="all, delete-orphan"
    )


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    video_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("videos.id"), index=True
    )
    type: Mapped[str] = mapped_column(String(50))
    # Type values: image, audio, music, clip
    url: Mapped[str] = mapped_column(Text)
    meta: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationships
    video: Mapped["Video"] = relationship(back_populates="assets")


class APIUsage(Base):
    __tablename__ = "api_usage"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    provider: Mapped[str] = mapped_column(String(50))
    # Provider values: replicate, elevenlabs, heygen, anthropic
    action: Mapped[str] = mapped_column(String(100))
    # Action values: image_gen, voice_gen, avatar_gen, script_gen
    project_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("projects.id"), nullable=True, index=True
    )
    cost_cents: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
