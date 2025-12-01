from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import get_settings
from database import init_db
from routers import auth, clients, projects, videos, webhooks

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if settings.debug:
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)},
        )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# Custom exceptions
class QuotaExceededError(Exception):
    pass


class NotFoundError(Exception):
    def __init__(self, resource: str, id: str):
        self.resource = resource
        self.id = id


@app.exception_handler(QuotaExceededError)
async def quota_handler(request: Request, exc: QuotaExceededError) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={"detail": "Monthly video quota exceeded"},
    )


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": f"{exc.resource} with id '{exc.id}' not found"},
    )


# Health check
@app.get("/health")
async def health_check() -> dict[str, Any]:
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": "0.1.0",
    }


# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(clients.router, prefix="/api/clients", tags=["clients"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(videos.router, prefix="/api/videos", tags=["videos"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["webhooks"])
