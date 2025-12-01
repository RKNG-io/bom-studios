# BOM Studios — Agent Coordination

## Quick Start

```bash
# Clone and setup
git clone <repo>
cd bom-studios

# Run specific agent
claude --skill skills/engine-agent    # Flet internal app
claude --skill skills/api-agent       # FastAPI backend
claude --skill skills/portal-agent    # Next.js client portal
claude --skill skills/pipeline-agent  # Video automation
```

---

## Agent Responsibilities

| Agent | Directory | Builds |
|-------|-----------|--------|
| **Engine** | `engine/` | Flet desktop app, provider integrations |
| **API** | `api/` | FastAPI backend, webhooks, assembly service |
| **Portal** | `portal/` | Next.js client-facing site |
| **Pipeline** | `automations/` | Prompts, n8n workflows, integration glue |

---

## Build Order (Recommended)

### Phase 0 — Foundation (Parallel)
```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ Engine      │   │ API         │   │ Portal      │
│ - Scaffold  │   │ - Scaffold  │   │ - Scaffold  │
│ - Theme     │   │ - Models    │   │ - Tailwind  │
│ - Layout    │   │ - DB        │   │ - Auth UI   │
└─────────────┘   └─────────────┘   └─────────────┘
```

### Phase 1 — Core Features (Sequential dependencies)
```
API (models, CRUD)
    ↓
Engine (video wizard, uses API for assembly)
    ↓
Portal (auth, dashboard, uses API)
```

### Phase 2.5 — Pipeline (After API stable)
```
Pipeline (prompts, n8n, uses API endpoints)
```

---

## Running Agents

### Option 1: Sequential (Safer)

```bash
# Day 1-2: Foundation
claude --skill skills/api-agent "Build Phase 0: scaffold, config, database, models"
claude --skill skills/engine-agent "Build Phase 0: app shell, theme, layout, placeholders"
claude --skill skills/portal-agent "Build Phase 0: scaffold, tailwind, login page"

# Day 3-5: API core
claude --skill skills/api-agent "Build Phase 1a: client, project, video CRUD endpoints"

# Day 6-10: Engine video flow
claude --skill skills/engine-agent "Build Phase 1a: video creation wizard"

# Day 11-14: Portal + Auth
claude --skill skills/api-agent "Build Phase 1c: magic link auth"
claude --skill skills/portal-agent "Build Phase 1c: auth flow, dashboard, video list"

# Day 15-20: Pipeline
claude --skill skills/pipeline-agent "Build prompts and test with sample inputs"
claude --skill skills/pipeline-agent "Build n8n workflow"
```

### Option 2: Parallel (Faster, needs coordination)

Run engine + api + portal simultaneously on Phase 0, then coordinate at integration points.

Use feature flags or mocks for cross-dependencies:
- Engine mocks API responses until API ready
- Portal mocks API responses until API ready
- Pipeline waits for API endpoints

---

## Inter-Agent Communication

Agents share data through:

1. **API endpoints** — Single source of truth
2. **Database** — SQLite file at `data/bom.db`
3. **Shared types** — `api/models/schemas.py` defines all data shapes

### Sync Points

| When | What | Who Updates |
|------|------|-------------|
| Model changes | Update Pydantic schemas | API Agent |
| New endpoint | Document in API spec | API Agent |
| UI needs data | Call existing endpoint or request new | Engine/Portal → API |
| Pipeline needs endpoint | Request or build | Pipeline → API |

---

## Verification Checklist

### After Phase 0
- [ ] `cd engine && flet run app.py` — App opens, navigation works
- [ ] `cd api && uvicorn main:app --reload` — Server starts, `/health` returns 200
- [ ] `cd portal && npm run dev` — Site loads, login page renders

### After Phase 1
- [ ] Can create a client via API
- [ ] Can create a project via API
- [ ] Engine shows project list
- [ ] Engine video wizard completes (mocked generation OK)

### After Phase 1c
- [ ] Portal login flow works (magic link)
- [ ] Client sees their videos
- [ ] Approval updates video status

### After Phase 2.5
- [ ] Form submission → script generated
- [ ] Script → images generated
- [ ] Images + audio → video assembled
- [ ] Draft appears in Engine review queue

---

## Debugging

### Agent stuck?
1. Check the relevant SKILL.md for guidance
2. Check `/docs/` for specs
3. Run tests: `pytest api/` or `npm test` in portal
4. Check logs for provider errors

### Integration failing?
1. Verify API is running
2. Check CORS settings in `api/main.py`
3. Verify environment variables set
4. Check database migrations ran

### Pipeline failing?
1. Test prompts in isolation first
2. Check n8n execution logs
3. Verify all API keys set
4. Check provider rate limits

---

## Environment Setup

```bash
# Copy env template
cp .env.example .env

# Required keys
ANTHROPIC_API_KEY=sk-ant-...
REPLICATE_API_TOKEN=r8_...
ELEVENLABS_API_KEY=...

# Optional (Phase 4)
STRIPE_SECRET_KEY=sk_...
RESEND_API_KEY=re_...
```

---

## File Outputs

All agents write to their designated directories:

```
bom-studios/
├── engine/          ← Engine Agent
├── api/             ← API Agent
├── portal/          ← Portal Agent
├── automations/     ← Pipeline Agent
├── data/            ← Shared database
└── docs/            ← Reference (read-only)
```

---

## Emergency Stops

If an agent is going off track:

1. Stop the agent
2. Review recent changes: `git diff`
3. Revert if needed: `git checkout -- <path>`
4. Add clarification to the SKILL.md
5. Resume with more specific instruction

---

## Success Criteria

**MVP Complete When:**
- [ ] Client fills Tally form
- [ ] Video draft appears in Engine within 10 minutes
- [ ] Jeroen reviews and approves in Engine
- [ ] Client sees video in Portal
- [ ] Client approves
- [ ] Video delivered to Drive

**Time Target:** 4–5 weeks to MVP
