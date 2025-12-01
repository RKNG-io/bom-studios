# CLAUDE.md — BOM Studios

## Project Overview

BOM Studios is an internal video production platform for a Dutch social media agency. It automates video creation from client intake to delivery.

**Three applications:**
- `engine/` — Flet desktop app (internal production tool)
- `api/` — FastAPI backend (shared services, webhooks, video assembly)
- `portal/` — Next.js client portal (login, approvals, downloads)

**Core automation flow:**
```
Client intake form (Tally) → n8n webhook → LLM script → LLM image prompts 
→ Replicate images → ElevenLabs VO → FFmpeg assembly → Review queue
```

---

## Tech Stack

| Layer | Tech |
|-------|------|
| Internal UI | Flet (Python) |
| Client Portal | Next.js 14, TypeScript, Tailwind |
| API | FastAPI, Python 3.11 |
| Database | SQLite (dev), PostgreSQL (prod) |
| Storage | Local filesystem, Google Drive (delivery) |
| Automation | n8n (orchestration), internal event bus |
| AI Providers | Replicate (Flux), ElevenLabs, HeyGen, Claude API |
| Video | FFmpeg, MoviePy |

---

## Directory Structure

```
bom-studios/
├── CLAUDE.md                 # This file
├── engine/                   # Flet internal app
│   ├── app.py               # Entrypoint
│   ├── ui/
│   │   ├── pages/           # Dashboard, Create, Projects, Library, Settings
│   │   ├── components/      # Buttons, Cards, Inputs, Modals
│   │   └── theme.py         # Design system tokens
│   ├── core/
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── database.py      # DB connection
│   │   ├── projects.py      # Project CRUD
│   │   ├── videos.py        # Video CRUD
│   │   └── costs.py         # API cost tracking
│   └── providers/
│       ├── replicate.py     # Image generation
│       ├── elevenlabs.py    # Voice generation
│       ├── heygen.py        # Avatar generation
│       └── drive.py         # Google Drive upload
│
├── api/                      # FastAPI backend
│   ├── main.py              # Entrypoint
│   ├── config.py            # Settings, env vars
│   ├── routers/
│   │   ├── auth.py          # Magic link auth
│   │   ├── projects.py      # Project endpoints
│   │   ├── videos.py        # Video endpoints
│   │   ├── webhooks.py      # n8n, Stripe, Tally
│   │   └── assembly.py      # Video assembly endpoint
│   ├── services/
│   │   ├── llm.py           # Claude API wrapper
│   │   ├── video.py         # FFmpeg assembly
│   │   └── notifications.py # Email, Slack
│   └── models/
│       └── schemas.py       # Pydantic models
│
├── portal/                   # Next.js client portal
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx         # Landing/login
│   │   ├── login/
│   │   ├── dashboard/
│   │   ├── videos/
│   │   └── approvals/
│   ├── components/
│   │   ├── ui/              # Design system components
│   │   └── ...
│   └── lib/
│       ├── api.ts           # API client
│       └── auth.ts          # Auth helpers
│
├── automations/
│   ├── prompts/             # LLM prompt templates
│   │   ├── script_generator.txt
│   │   └── image_prompts.txt
│   └── n8n/                 # n8n workflow exports
│
├── data/
│   └── bom.db               # SQLite database
│
├── scripts/
│   ├── setup.sh             # Dev environment setup
│   └── seed.py              # Seed test data
│
└── docs/
    ├── brand-kit.md
    ├── design-system.md
    ├── engine-spec.md
    └── auto-pipeline.md
```

---

## Design System Reference

**Colours:**
| Name | Hex |
|------|-----|
| BOM Black | #0C0C0C |
| Warm White | #FAF9F7 |
| Paper White | #FFFFFF |
| Slate Grey | #2E2E2E |
| Steel Grey | #5A5A5A |
| Silver Mist | #E8E6E3 |
| Stone Blue | #6B8EA3 |
| Sage | #9BA88A |

**Typography:**
- Headings: Michroma
- Body: Inter, 16–18px, line-height 1.5

**Icons:** Lucide React (portal), Lucide (engine via SVG)

**Spacing:** 8px base — 8, 16, 24, 32, 48, 64, 96

---

## Environment Variables

```bash
# Database
DATABASE_URL=sqlite:///./data/bom.db

# API Keys
REPLICATE_API_TOKEN=
ELEVENLABS_API_KEY=
HEYGEN_API_KEY=
ANTHROPIC_API_KEY=

# Google
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_DRIVE_FOLDER_ID=

# Auth
JWT_SECRET=
MAGIC_LINK_SECRET=

# External
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
RESEND_API_KEY=

# n8n
N8N_WEBHOOK_URL=
```

---

## Commands

```bash
# Engine (Flet)
cd engine && flet run app.py
cd engine && flet run app.py --web  # Browser mode

# API
cd api && uvicorn main:app --reload --port 8000

# Portal
cd portal && npm run dev

# Database
cd api && alembic upgrade head        # Run migrations
cd api && python -m scripts.seed      # Seed data

# Video assembly (requires FFmpeg)
ffmpeg -version  # Verify installed
```

---

## Data Models (Core)

```python
class Client:
    id: str (uuid)
    name: str
    email: str
    brand_kit: JSON  # {logo_url, colours, fonts}
    package: str     # kickstart, growth, pro
    created_at: datetime

class Project:
    id: str (uuid)
    client_id: str (FK)
    name: str
    status: str      # draft, in_progress, review, approved, delivered
    created_at: datetime

class Video:
    id: str (uuid)
    project_id: str (FK)
    title: str
    script: JSON     # {hook, scenes[], cta}
    status: str      # scripting, generating, rendering, draft, approved, delivered
    formats: JSON    # {vertical: url, square: url, horizontal: url}
    cost_cents: int
    created_at: datetime

class Asset:
    id: str (uuid)
    video_id: str (FK)
    type: str        # image, audio, music, clip
    url: str
    metadata: JSON
    created_at: datetime

class APIUsage:
    id: str (uuid)
    provider: str    # replicate, elevenlabs, heygen, anthropic
    action: str      # image_gen, voice_gen, script_gen
    project_id: str (FK, nullable)
    cost_cents: int
    created_at: datetime
```

---

## API Endpoints (Key)

```
POST   /api/auth/magic-link     # Send magic link
GET    /api/auth/verify         # Verify token
GET    /api/projects            # List projects
POST   /api/projects            # Create project
GET    /api/projects/{id}       # Get project
GET    /api/videos              # List videos
POST   /api/videos              # Create video
PATCH  /api/videos/{id}         # Update video status
POST   /api/videos/{id}/approve # Client approval
POST   /api/assembly/generate   # Trigger video assembly
POST   /api/webhooks/tally      # Intake form webhook
POST   /api/webhooks/stripe     # Payment webhook
```

---

## Current Priority: Phase 0 + 1a

**Immediate tasks:**

1. **Scaffold all three apps** — Flet, FastAPI, Next.js running locally
2. **Database + models** — SQLAlchemy setup, initial migration
3. **Engine UI skeleton** — Navigation, placeholder pages, theme
4. **Portal login page** — Basic auth flow (magic link)
5. **Simple video creation** — Script input → Replicate images → Upload VO → Preview

**Do NOT build yet:**
- n8n automation (Phase 2.5)
- HeyGen integration (Phase 2b)
- Stripe billing (Phase 4)
- Full CRM

---

## Code Style

- **Python:** Black formatter, 88 line length, type hints required
- **TypeScript:** Prettier, strict mode, no `any`
- **Commits:** Conventional commits (`feat:`, `fix:`, `chore:`)
- **Files:** Lowercase with underscores (Python), lowercase with hyphens (TS)

---

## Testing Approach

- Unit tests for core logic (pytest)
- API tests for endpoints (pytest + httpx)
- Manual testing for UI (Flet is hard to test)
- Portal: Playwright for critical flows (login, approval)

---

## When Stuck

1. Check `/docs/` for specs
2. Check this file for structure
3. If unclear, ask — don't guess on business logic
4. If blocked on external API, stub it and move on

---

## Agent Coordination

This project uses multiple skill agents. See `/skills/` for:
- `engine-agent/` — Flet UI and internal logic
- `api-agent/` — FastAPI backend
- `portal-agent/` — Next.js frontend
- `pipeline-agent/` — Video automation pipeline

Each agent has its own SKILL.md with focused instructions.
