import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import get_settings

settings = get_settings()

# Determine database URL - handle container environments
database_url = settings.database_url

if "sqlite" in database_url and ":memory:" not in database_url:
    db_path = database_url.replace("sqlite+aiosqlite:///", "")
    if db_path.startswith("./"):
        db_path = db_path[2:]
    db_dir = Path(db_path).parent
    try:
        db_dir.mkdir(parents=True, exist_ok=True)
        # Test if we can write to this directory
        test_file = db_dir / ".write_test"
        test_file.touch()
        test_file.unlink()
    except (OSError, PermissionError):
        # Fall back to /tmp for container environments
        tmp_path = Path("/tmp/bom_data")
        tmp_path.mkdir(parents=True, exist_ok=True)
        database_url = f"sqlite+aiosqlite:///{tmp_path}/bom.db"
        print(f"Using temp database at {database_url}")

engine = create_async_engine(
    database_url,
    echo=settings.debug,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@asynccontextmanager
async def get_session_context() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
