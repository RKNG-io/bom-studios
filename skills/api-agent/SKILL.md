# SKILL.md — API Agent

## Role

Build and maintain the FastAPI backend that serves both the Engine and Portal, handles webhooks, and orchestrates video assembly.

---

## Scope

- `api/` directory only
- REST endpoints for projects, videos, clients
- Authentication (magic link)
- Webhook handlers (Tally, Stripe, n8n)
- Video assembly service (FFmpeg)
- LLM service (Claude API for script generation)
- Notification service (email, Slack)

**Out of scope:** Flet UI, Next.js portal, n8n workflow configuration

---

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy 2.0 (async)
- Pydantic v2
- httpx (async HTTP)
- FFmpeg + MoviePy (video assembly)
- Resend (email)

---

## File Structure

```
api/
├── main.py                   # FastAPI app entrypoint
├── config.py                 # Settings from env vars
├── database.py               # Async SQLAlchemy setup
├── models/
│   ├── db.py                 # SQLAlchemy models
│   └── schemas.py            # Pydantic request/response models
├── routers/
│   ├── auth.py               # Magic link authentication
│   ├── clients.py            # Client CRUD
│   ├── projects.py           # Project CRUD
│   ├── videos.py             # Video CRUD + approval
│   ├── webhooks.py           # Tally, Stripe, n8n
│   └── assembly.py           # Video assembly trigger
├── services/
│   ├── auth.py               # Token generation/verification
│   ├── llm.py                # Claude API wrapper
│   ├── video.py              # FFmpeg assembly logic
│   ├── notifications.py      # Email, Slack
│   └── storage.py            # File storage, Drive upload
├── middleware/
│   └── auth.py               # JWT verification middleware
└── utils/
    └── costs.py              # API cost logging
```

---

## Task Queue

### Phase 0 (Foundation)

- [ ] `main.py` — FastAPI app with CORS, error handling
- [ ] `config.py` — Pydantic Settings from .env
- [ ] `database.py` — Async SQLAlchemy engine + session
- [ ] `models/db.py` — Client, Project, Video, Asset, APIUsage
- [ ] `models/schemas.py` — Pydantic models for all entities
- [ ] Health check endpoint: `GET /health`

### Phase 1a (Core CRUD)

- [ ] `routers/clients.py` — List, create, get, update
- [ ] `routers/projects.py` — List, create, get, update, delete
- [ ] `routers/videos.py` — List, create, get, update status

### Phase 1c (Auth + Portal Support)

- [ ] `services/auth.py` — Magic link token generation
- [ ] `routers/auth.py` — `POST /auth/magic-link`, `GET /auth/verify`
- [ ] `middleware/auth.py` — JWT verification
- [ ] `routers/videos.py` — `POST /videos/{id}/approve` (client approval)

### Phase 2.5 (Pipeline)

- [ ] `routers/webhooks.py` — `POST /webhooks/tally` (intake form)
- [ ] `services/llm.py` — Script generation, image prompt generation
- [ ] `routers/assembly.py` — `POST /assembly/generate`
- [ ] `services/video.py` — FFmpeg assembly from images + audio

### Phase 4 (Billing)

- [ ] `routers/webhooks.py` — `POST /webhooks/stripe`
- [ ] Invoice endpoints (stretch)

---

## API Design

### Authentication

```
POST /api/auth/magic-link
Body: { "email": "client@example.com" }
Response: { "message": "Magic link sent" }

GET /api/auth/verify?token=xxx
Response: { "access_token": "jwt...", "client": {...} }
```

### Clients

```
GET    /api/clients                 # List all (internal only)
POST   /api/clients                 # Create client
GET    /api/clients/{id}            # Get client
PATCH  /api/clients/{id}            # Update client
```

### Projects

```
GET    /api/projects                # List (filterable by client, status)
POST   /api/projects                # Create project
GET    /api/projects/{id}           # Get with videos
PATCH  /api/projects/{id}           # Update status
DELETE /api/projects/{id}           # Soft delete
```

### Videos

```
GET    /api/videos                  # List (filterable)
POST   /api/videos                  # Create video record
GET    /api/videos/{id}             # Get video detail
PATCH  /api/videos/{id}             # Update (status, script, etc.)
POST   /api/videos/{id}/approve     # Client approval (authed)
POST   /api/videos/{id}/reject      # Client rejection with note
```

### Assembly

```
POST /api/assembly/generate
Body: {
    "video_id": "uuid",
    "script": { "hook": "...", "scenes": [...], "cta": "..." },
    "images": ["url1", "url2", ...],
    "audio_url": "https://...",
    "music_url": "https://..." (optional),
    "format": "vertical"  # vertical, square, horizontal
}
Response: { "job_id": "uuid", "status": "processing" }

GET /api/assembly/status/{job_id}
Response: { "status": "complete", "output_url": "https://..." }
```

### Webhooks

```
POST /api/webhooks/tally
Body: (Tally form submission payload)
→ Triggers pipeline: parse → LLM → images → VO → assembly

POST /api/webhooks/stripe
Body: (Stripe webhook payload)
→ Updates invoice status

POST /api/webhooks/n8n
Body: { "event": "...", "data": {...} }
→ Generic n8n callback
```

---

## Pydantic Schemas

```python
# models/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    package: str = "kickstart"
    brand_kit: Optional[dict] = None

class ClientResponse(BaseModel):
    id: str
    name: str
    email: str
    package: str
    brand_kit: Optional[dict]
    created_at: datetime

class ProjectCreate(BaseModel):
    client_id: str
    name: str

class ProjectResponse(BaseModel):
    id: str
    client_id: str
    name: str
    status: str
    created_at: datetime

class VideoCreate(BaseModel):
    project_id: str
    title: str
    script: Optional[dict] = None

class VideoResponse(BaseModel):
    id: str
    project_id: str
    title: str
    script: Optional[dict]
    status: str
    formats: Optional[dict]
    cost_cents: int
    created_at: datetime

class VideoApproval(BaseModel):
    approved: bool
    note: Optional[str] = None

class AssemblyRequest(BaseModel):
    video_id: str
    script: dict
    images: list[str]
    audio_url: str
    music_url: Optional[str] = None
    format: str = "vertical"

class ScriptGenerationRequest(BaseModel):
    business_name: str
    what_they_sell: str
    target_customer: str
    differentiator: str
    tone: str = "friendly"
    language: str = "EN"
    topic: Optional[str] = None
```

---

## LLM Service

```python
# services/llm.py
import anthropic
from config import settings

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

SCRIPT_PROMPT = """You are a short-form video scriptwriter...
[full prompt from pipeline spec]
"""

async def generate_script(context: dict) -> dict:
    prompt = SCRIPT_PROMPT.format(**context)
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    
    # Parse JSON from response
    import json
    return json.loads(response.content[0].text)

async def generate_image_prompts(script: dict, brand_context: dict) -> list[str]:
    # Similar pattern
    ...
```

---

## Video Assembly Service

```python
# services/video.py
import subprocess
import tempfile
from pathlib import Path

async def assemble_video(
    images: list[str],
    audio_url: str,
    output_format: str = "vertical",
    music_url: str = None,
) -> str:
    """
    Assemble video from images and audio using FFmpeg.
    Returns path to output file.
    """
    
    # Download assets to temp dir
    temp_dir = Path(tempfile.mkdtemp())
    
    # Download images
    image_paths = []
    for i, url in enumerate(images):
        path = temp_dir / f"img_{i:03d}.png"
        # Download with httpx
        image_paths.append(path)
    
    # Download audio
    audio_path = temp_dir / "audio.mp3"
    # Download with httpx
    
    # Calculate durations (equal split for now)
    duration_per_image = 5  # seconds, or calculate from audio length
    
    # Build FFmpeg command
    # Create image sequence with durations
    # Add Ken Burns effect (zoom/pan)
    # Overlay audio
    # Add music (reduced volume)
    # Export
    
    output_path = temp_dir / "output.mp4"
    
    cmd = [
        "ffmpeg",
        "-y",  # Overwrite
        # ... complex filter chain
        str(output_path),
    ]
    
    subprocess.run(cmd, check=True)
    
    return str(output_path)
```

---

## Webhook Handler Pattern

```python
# routers/webhooks.py
from fastapi import APIRouter, BackgroundTasks, HTTPException
from services.llm import generate_script, generate_image_prompts
from services.video import assemble_video

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

@router.post("/tally")
async def handle_tally_webhook(
    payload: dict,
    background_tasks: BackgroundTasks,
):
    """
    Handle Tally form submission.
    Triggers full video generation pipeline in background.
    """
    
    # Parse form fields
    context = parse_tally_payload(payload)
    
    # Validate client exists or create
    client = await get_or_create_client(context["email"])
    
    # Check quota
    if await client_over_quota(client.id):
        # Send rejection email
        return {"status": "rejected", "reason": "quota_exceeded"}
    
    # Queue pipeline
    background_tasks.add_task(
        run_video_pipeline,
        client_id=client.id,
        context=context,
    )
    
    return {"status": "accepted", "message": "Video generation started"}

async def run_video_pipeline(client_id: str, context: dict):
    """Background task: full pipeline execution."""
    
    # 1. Generate script
    script = await generate_script(context)
    
    # 2. Generate image prompts
    prompts = await generate_image_prompts(script, context)
    
    # 3. Generate images (parallel)
    images = await generate_images_parallel(prompts)
    
    # 4. Generate voiceover
    audio_url = await generate_voiceover(script)
    
    # 5. Assemble video
    video_path = await assemble_video(images, audio_url)
    
    # 6. Upload to storage
    video_url = await upload_to_storage(video_path)
    
    # 7. Create video record
    video = await create_video_record(
        client_id=client_id,
        script=script,
        video_url=video_url,
        status="draft",
    )
    
    # 8. Notify Jeroen
    await send_notification(
        channel="slack",
        message=f"New draft video ready: {video.id}",
    )
```

---

## Error Handling

```python
# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log error
    print(f"Unhandled error: {exc}")
    
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# Specific exceptions
class QuotaExceededError(Exception):
    pass

@app.exception_handler(QuotaExceededError)
async def quota_handler(request: Request, exc: QuotaExceededError):
    return JSONResponse(
        status_code=429,
        content={"detail": "Monthly video quota exceeded"},
    )
```

---

## Testing

```bash
# Run server
cd api && uvicorn main:app --reload

# Test endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/clients -d '{"name":"Test","email":"test@example.com"}'

# Run tests
cd api && pytest
```

---

## Handoff Points

- **From Engine Agent:** Engine calls API for video assembly, project sync
- **To Engine Agent:** Webhook creates project → Engine sees it on refresh
- **From Portal Agent:** Portal calls API for auth, videos, approvals
- **To Portal Agent:** Video status changes reflect in portal
- **From n8n:** Webhooks trigger pipeline
- **To n8n:** Events emitted for downstream automation

---

## When Stuck

1. Check FastAPI docs: https://fastapi.tiangolo.com/
2. Check `/docs/bom-studios-engine-spec.md` for data models
3. Check `/docs/bom-studios-auto-pipeline.md` for pipeline logic
4. If external API unclear, stub the response
