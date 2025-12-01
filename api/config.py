from functools import lru_cache
from typing import Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_DATABASE_URL = "sqlite+aiosqlite:///./data/bom.db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_name: str = "BOM Studios API"
    debug: bool = False

    # Database
    database_url: str = DEFAULT_DATABASE_URL

    @field_validator("database_url", mode="before")
    @classmethod
    def default_database_url(cls, v: str) -> str:
        """Use default if empty string is provided."""
        if v == "" or v is None:
            return DEFAULT_DATABASE_URL
        return v

    # Auth
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 1 week
    magic_link_secret: str = "change-me-in-production"
    magic_link_expire_minutes: int = 15

    # API Keys (optional, for future phases)
    replicate_api_token: Optional[str] = None
    elevenlabs_api_key: Optional[str] = None
    heygen_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    # Google Drive (optional, for future phases)
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    google_drive_folder_id: Optional[str] = None

    # External services (optional, for future phases)
    stripe_secret_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None
    resend_api_key: Optional[str] = None
    n8n_webhook_url: Optional[str] = None

    # CORS
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "https://bom-studios.vercel.app",
        "https://*.vercel.app",
    ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
