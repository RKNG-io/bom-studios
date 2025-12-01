# BOM Studios — Broad Platform Scaffolding Plan

Multi-agent parallel execution strategy for scaffolding all platform components.

---

## Overview

| App | Tech | Directory | Status |
|-----|------|-----------|--------|
| Website | Next.js 14, Tailwind | `website/` | ✅ Complete |
| API | FastAPI, SQLAlchemy | `api/` | 🔲 Pending |
| Portal | Next.js 14, Tailwind | `portal/` | 🔲 Pending |
| Engine | Flet (Python) | `engine/` | 🔲 Pending |
| Pipeline | n8n, Prompts | `automations/` | 🔲 Pending |

---

## Phase 1: API + Portal + Engine Scaffolds (Parallel)

Run 4 agents simultaneously:

### Agent 1: API Foundation
**Directory:** `/Users/liz/Projects/bom-studios/api`

**Creates:**
```
api/
├── main.py                 # FastAPI app, CORS, health check
├── config.py               # Pydantic Settings from .env
├── database.py             # Async SQLAlchemy engine + session
├── models/
│   ├── __init__.py
│   ├── db.py               # SQLAlchemy models (Client, Project, Video, Asset, APIUsage)
│   └── schemas.py          # Pydantic request/response models
├── routers/
│   ├── __init__.py
│   ├── health.py           # Health check endpoint
│   └── clients.py          # Client CRUD (placeholder)
├── requirements.txt        # Dependencies
└── .env.example            # Environment template
```

**Key dependencies:**
- fastapi, uvicorn
- sqlalchemy[asyncio], aiosqlite
- pydantic, pydantic-settings
- httpx, python-multipart

---

### Agent 2: API Routes
**Directory:** `/Users/liz/Projects/bom-studios/api`

**Creates:**
```
api/routers/
├── auth.py                 # Magic link endpoints
├── projects.py             # Project CRUD
├── videos.py               # Video CRUD + approval
└── webhooks.py             # Tally, Stripe placeholders
```

**Also creates:**
```
api/services/
├── __init__.py
├── auth.py                 # Token generation/verification
└── notifications.py        # Email placeholder
```

---

### Agent 3: Portal Foundation
**Directory:** `/Users/liz/Projects/bom-studios/portal`

**Creates:**
```
portal/
├── package.json
├── tsconfig.json
├── tailwind.config.ts      # Same tokens as website
├── postcss.config.js
├── next.config.js
├── app/
│   ├── layout.tsx          # Root layout (simpler than website)
│   ├── globals.css
│   ├── page.tsx            # Redirect to /login or /dashboard
│   ├── login/
│   │   └── page.tsx        # Magic link form
│   └── (authenticated)/
│       ├── layout.tsx      # Protected layout
│       └── dashboard/
│           └── page.tsx    # Client dashboard shell
├── components/
│   └── ui/                 # Copy from website or shared
├── lib/
│   ├── api.ts              # API client
│   ├── auth.ts             # Auth helpers
│   └── utils.ts
└── types/
    └── index.ts
```

---

### Agent 4: Engine Foundation
**Directory:** `/Users/liz/Projects/bom-studios/engine`

**Creates:**
```
engine/
├── app.py                  # Flet entrypoint
├── requirements.txt
├── ui/
│   ├── __init__.py
│   ├── theme.py            # Design tokens
│   ├── layout.py           # App shell with sidebar
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── dashboard.py    # Placeholder
│   │   ├── create_video.py # Placeholder
│   │   ├── projects.py     # Placeholder
│   │   ├── library.py      # Placeholder
│   │   └── settings.py     # Placeholder
│   └── components/
│       ├── __init__.py
│       ├── sidebar.py      # Navigation
│       └── button.py       # Primary, secondary
├── core/
│   ├── __init__.py
│   ├── database.py         # SQLite connection
│   └── models.py           # SQLAlchemy models (shared with API)
└── providers/
    ├── __init__.py
    └── base.py             # Base provider class
```

---

## Phase 2: API Completion + Portal Auth (Parallel)

### Agent 5: API Services
**Adds to:** `/Users/liz/Projects/bom-studios/api`

**Creates:**
```
api/services/
├── llm.py                  # Claude API wrapper
├── video.py                # FFmpeg assembly logic
└── storage.py              # File storage helpers
```

**Also:**
- Complete auth flow with JWT
- Middleware for protected routes

---

### Agent 6: Portal Auth + Dashboard
**Adds to:** `/Users/liz/Projects/bom-studios/portal`

**Creates:**
```
portal/
├── app/
│   ├── verify/
│   │   └── page.tsx        # Token verification
│   └── (authenticated)/
│       ├── videos/
│       │   ├── page.tsx    # Video list
│       │   └── [id]/
│       │       └── page.tsx # Video detail + approval
│       └── settings/
│           └── page.tsx
├── components/
│   ├── video-card.tsx
│   ├── video-player.tsx
│   ├── approval-form.tsx
│   └── status-badge.tsx
└── hooks/
    ├── use-auth.ts
    └── use-videos.ts
```

---

## Phase 3: Engine Features + Pipeline (Parallel)

### Agent 7: Engine Video Wizard
**Adds to:** `/Users/liz/Projects/bom-studios/engine`

**Completes:**
- `ui/pages/create_video.py` — Full 5-step wizard
- `ui/pages/projects.py` — Project list + detail
- `ui/pages/library.py` — Video grid

---

### Agent 8: Engine Providers
**Adds to:** `/Users/liz/Projects/bom-studios/engine`

**Creates:**
```
engine/providers/
├── replicate.py            # Image generation
├── elevenlabs.py           # Voice generation
└── drive.py                # Google Drive upload
```

---

### Agent 9: Pipeline Foundation
**Directory:** `/Users/liz/Projects/bom-studios/automations`

**Creates:**
```
automations/
├── prompts/
│   ├── script_generator.md
│   ├── image_prompts.md
│   └── caption_generator.md
├── schemas/
│   ├── tally_payload.json
│   ├── script_output.json
│   └── pipeline_events.json
├── n8n/
│   └── README.md           # Setup instructions
└── tests/
    ├── test_prompts.py
    └── mock_payloads/
        └── coffee_shop.json
```

---

## Execution Commands

### Phase 1 (4 parallel agents)
```
Agent 1: API Foundation
Agent 2: API Routes
Agent 3: Portal Foundation
Agent 4: Engine Foundation
```

### Phase 2 (2 parallel agents)
```
Agent 5: API Services
Agent 6: Portal Auth + Dashboard
```

### Phase 3 (3 parallel agents)
```
Agent 7: Engine Video Wizard
Agent 8: Engine Providers
Agent 9: Pipeline Foundation
```

---

## Shared Resources

### Database Schema (shared between API + Engine)
```python
# Client, Project, Video, Asset, APIUsage
# Defined once in api/models/db.py
# Engine imports or duplicates for local SQLite
```

### Design Tokens (shared between Website + Portal)
```typescript
// Same Tailwind config
// Can be extracted to shared package later
```

### Types (shared between Portal + API)
```typescript
// Portal types mirror Pydantic schemas
// Can generate from OpenAPI spec later
```

---

## Dependencies Between Agents

```
Phase 1:
  Agent 1 (API Foundation) ──┐
  Agent 2 (API Routes)    ───┼── Independent, merge after
  Agent 3 (Portal)        ───┤
  Agent 4 (Engine)        ───┘

Phase 2:
  Agent 5 (API Services)  ─── Depends on Phase 1 API
  Agent 6 (Portal Auth)   ─── Depends on Phase 1 Portal + API

Phase 3:
  Agent 7 (Engine Wizard) ─── Depends on Phase 1 Engine
  Agent 8 (Engine Providers) ─ Depends on Phase 1 Engine
  Agent 9 (Pipeline)      ─── Depends on Phase 2 API Services
```

---

## Post-Scaffold Verification

After each phase, verify:

### Phase 1 Complete
```bash
# API
cd api && pip install -r requirements.txt
uvicorn main:app --reload
# → http://localhost:8000/health returns 200

# Portal
cd portal && npm install && npm run dev
# → http://localhost:3000 shows login page

# Engine
cd engine && pip install -r requirements.txt
flet run app.py
# → Window opens with sidebar navigation
```

### Phase 2 Complete
```bash
# API auth works
curl -X POST http://localhost:8000/api/auth/magic-link -d '{"email":"test@example.com"}'

# Portal auth flow works
# → Can log in with magic link
```

### Phase 3 Complete
```bash
# Engine can create video (mocked)
# Pipeline prompts return valid JSON
python -c "from automations.tests.test_prompts import test_script_generation; test_script_generation()"
```

---

## Estimated Effort

| Phase | Agents | Parallel Time |
|-------|--------|---------------|
| 1 | 4 | ~10 min |
| 2 | 2 | ~8 min |
| 3 | 3 | ~10 min |
| **Total** | **9** | **~30 min** |

Sequential would be ~2+ hours. Parallel saves significant time.

---

## Ready to Execute?

Say "run phase 1" to launch 4 agents for API + Portal + Engine scaffolds.
