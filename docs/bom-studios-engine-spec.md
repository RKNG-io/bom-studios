# BOM Studios Engine — Technical Spec (Refined)

---

## Overview

Internal production platform for BOM Studios. Handles video creation, client delivery, and content operations.

**Users:**
- Jeroen (production, client comms)
- You (strategy, automation, oversight)
- Clients (portal access for approvals and downloads)

**Stack:**
- Frontend: Flet (internal app), Next.js (client portal)
- Backend: FastAPI
- Database: SQLite → PostgreSQL when needed
- Storage: Google Drive (client delivery), local (working files)
- Automation: n8n (external triggers), internal event bus

---

## Architecture

```
bom-studios/
├── engine/                    # Flet internal app
│   ├── app.py
│   ├── ui/
│   │   ├── pages/
│   │   ├── components/
│   │   └── theme.py
│   ├── core/
│   │   ├── models.py
│   │   ├── projects.py
│   │   ├── videos.py
│   │   └── costs.py
│   └── providers/
│       ├── replicate.py
│       ├── elevenlabs.py
│       ├── heygen.py
│       └── drive.py
│
├── api/                       # FastAPI backend
│   ├── main.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── projects.py
│   │   ├── videos.py
│   │   └── webhooks.py
│   └── services/
│
├── portal/                    # Next.js client portal
│   ├── app/
│   │   ├── login/
│   │   ├── dashboard/
│   │   ├── videos/
│   │   └── approvals/
│   └── components/
│
├── automations/
│   ├── events.py
│   └── n8n_schemas/
│
└── data/
    └── bom.db
```

---

## Phase 0 — Foundation (3–5 days)

**Goal:** Skeleton that runs, navigation that works.

### Flet App
- App shell with sidebar navigation
- Theme from design system (colours, typography)
- Placeholder pages: Dashboard, Create, Projects, Library, Settings
- Basic responsive layout

### API
- FastAPI scaffold
- Health check endpoint
- SQLite connection
- Base models: Client, Project, Video

### Portal
- Next.js scaffold
- Login page (email + magic link or simple password)
- Authenticated layout shell
- "Coming soon" dashboard

**Outcome:** All three apps run locally. Navigation works. No functionality yet.

---

## Phase 1a — Simple Video Flow (1–2 weeks)

**Goal:** Produce a video without AI dependencies.

### Video Types

Not every video needs AI. Define three tracks:

| Type | Flow |
|------|------|
| **Image + VO** | Script → Generate images (Replicate) → Record/upload VO → Assemble → Export |
| **Stock + VO** | Script → Select stock footage → Record/upload VO → Assemble → Export |
| **Raw Edit** | Upload raw clips → Trim/arrange → Add captions → Export |

Phase 1a implements **Image + VO** only.

### Create Video Wizard (v1)

```
Step 1: Script
  - Text input
  - Character count
  - Save draft

Step 2: Visuals
  - Generate images from script (Replicate Flux)
  - Preview grid
  - Regenerate individual images
  - Reorder

Step 3: Audio
  - Upload audio file
  - OR record in browser (stretch)
  - Sync timing (manual markers)

Step 4: Preview
  - Assembled preview
  - Adjust timing
  - Add music track (upload or select from library)

Step 5: Export
  - 9:16 (Reels/TikTok/Shorts)
  - 1:1 (Feed)
  - 16:9 (YouTube)
  - Select formats, queue render
```

### Cost Tracking (Critical)

Every API call logged:

```python
class APIUsage:
    provider: str        # replicate, elevenlabs, heygen
    action: str          # image_gen, voice_gen, avatar_render
    project_id: str
    cost_cents: int
    created_at: datetime
```

Dashboard widget: "API spend this month: €XX"

Per-project view: "This project has cost €XX in API calls"

### Data Models

```python
class Client:
    id, name, email, brand_kit, created_at

class Project:
    id, client_id, name, status, created_at
    # status: draft, in_progress, review, approved, delivered

class Video:
    id, project_id, title, script, status, formats, created_at
    # status: scripting, generating, rendering, ready, delivered

class Asset:
    id, video_id, type, url, metadata
    # type: image, audio, music, clip
```

**Outcome:** Can produce an image-based video with uploaded voiceover. Costs tracked.

---

## Phase 1b — Projects & Library (1 week)

### Projects Page
- List all projects grouped by status
- Create new project (select client, name, package tier)
- Project detail view:
  - Client info
  - Videos in project
  - Status timeline
  - Cost summary
  - Delivery history

### Content Library
- All exported videos
- Filter: client, date, format, status
- Actions: preview, download, duplicate, push to Drive

### Client Management
- Simple client list
- Add/edit client
- Brand kit upload (logo, colours, fonts)
- Link to client portal account

**Outcome:** Organised project workflow. Content findable.

---

## Phase 1c — Client Portal v1 (1 week)

### Authentication
- Magic link email (Resend or similar)
- Session-based auth
- Clients created in engine, portal login auto-provisioned

### Client Dashboard
- Active project status
- Videos pending approval
- Approved videos (download links)
- Simple message/note to Jeroen

### Approval Flow
- View video preview
- Approve / Request changes (with text note)
- Approval triggers:
  - Status update in engine
  - Notification to Jeroen
  - (Phase 3) Auto-push to Drive

### Website Integration
- "Client Login" button in website header/footer
- Links to portal.bomstudios.nl (or /portal route)

**Outcome:** Clients can log in, see their videos, approve or request changes.

---

## Phase 2a — AI Voiceover (1 week)

### ElevenLabs Integration
- Voice library (presets for Dutch, English, male, female)
- Generate VO from script
- Preview before committing (cost control)
- Replace uploaded audio with generated

### Wizard Update
Step 3 becomes:
```
Audio
  ├── Upload file
  ├── Record in browser
  └── Generate with AI
        ├── Select voice
        ├── Preview (free tier if available, else warn of cost)
        └── Generate full
```

### Cost Control
- Show estimated cost before generation
- "This will cost approximately €0.XX. Proceed?"
- Log actual cost after generation

**Outcome:** Can generate voiceovers. Cost-aware.

---

## Phase 2b — AI Avatar (1 week)

### HeyGen Integration
- Avatar library (licensed avatars)
- Background options
- Generate avatar clip from script

### Wizard Update
New video type: **Avatar + VO**

```
Step 1: Script
Step 2: Avatar
  ├── Select avatar
  ├── Select background
  └── Generate (with cost warning)
Step 3: Visuals (optional B-roll)
Step 4: Preview + Edit
Step 5: Export
```

### Cost Control
- HeyGen is expensive. Show cost estimate prominently.
- Require confirmation before generation.
- Consider: draft renders at lower quality first?

**Outcome:** Can produce avatar videos. Cost-controlled.

---

## Phase 3 — Posting & Delivery (2 weeks)

### Content Calendar
- Monthly/weekly view
- Drag videos to date slots
- Status: scheduled, posted, skipped

### Caption Generator
- Generate caption from script
- Hashtag suggestions
- Platform variants (IG, TikTok, LinkedIn)
- Edit and save

### Delivery Automation
- On approval:
  - Copy to client's Google Drive folder
  - Send email with links
  - Update status
- On scheduled date:
  - Reminder notification
  - Checklist for manual posting
  - (Stretch) Direct posting via APIs where available

### Client Portal v2
- View scheduled content calendar
- Download approved videos by date
- View captions and posting notes

**Outcome:** Content operations system. Clients see what's coming.

---

## Phase 4 — Automation & Billing (2–3 weeks)

### n8n Integration
Events emitted:
- `video.exported`
- `video.approved`
- `video.delivered`
- `project.created`
- `invoice.paid`

Webhooks received:
- Stripe payment confirmation
- Client form submissions (Tally)

### Stripe Billing
- Create invoice from project
- Payment links
- Paid/unpaid status sync
- Monthly subscription support

### Notifications
- Email (Resend)
- Slack (internal)
- WhatsApp (stretch, via Twilio)

### Analytics Import (Stretch)
- Pull basic metrics from IG/TikTok
- Display in client portal
- Monthly summary generation

**Outcome:** Semi-autonomous operations. Billing integrated.

---

## What We're NOT Building (Yet)

| Feature | Why Not |
|---------|---------|
| Full CRM | 24 clients don't need Mailchimp. Use Notion. |
| AI caption coach | Nice to have. Phase 5. |
| Trend scraping | Manual curation is fine at this scale. |
| Auto-posting to all platforms | API access is inconsistent. Manual posting with good tooling is fine. |
| Custom client onboarding flows | Tally form → n8n → Notion is enough. |

---

## Timeline Summary

| Phase | Scope | Duration |
|-------|-------|----------|
| 0 | Foundation (Flet, API, Portal shells) | 3–5 days |
| 1a | Simple video flow (Image + VO) | 1–2 weeks |
| 1b | Projects, clients, library | 1 week |
| 1c | Client portal v1 (login, approvals) | 1 week |
| 2a | ElevenLabs voiceover | 1 week |
| 2b | HeyGen avatar | 1 week |
| 3 | Posting planner, calendar, delivery | 2 weeks |
| 4 | Automation, Stripe, notifications | 2–3 weeks |

**Total: 10–13 weeks** for full system.

**MVP (Phases 0–1c): 4–5 weeks** — can produce and deliver videos to clients.

---

## Open Questions

1. **Hosting:** Flet app runs locally or deployed? (Recommend: local for now, API + Portal on Railway/Vercel)
2. **Drive structure:** One folder per client, or per project?
3. **Portal domain:** portal.bomstudios.nl or bomstudios.nl/portal?
4. **Avatar licensing:** Which HeyGen avatars are cleared for client use?
5. **Music library:** License-free library to bundle, or client uploads only?

---

*End of spec.*
