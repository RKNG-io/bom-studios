# BOM Studios — Automated Video Pipeline

---

## Overview

Client submits intake form → API triggers pipeline → draft video generated → Jeroen reviews → client approves → delivered.

**Human touchpoints:** Review and approval only. Everything else automated.

---

## Current Implementation Status

| Component | Status | Location |
|-----------|--------|----------|
| Website + Intake Form | ✅ Live | https://bom-studios.vercel.app |
| Client Portal | ✅ Live | https://bom-studios.vercel.app/login |
| Engine (Review Tool) | ✅ Built | `/engine` (desktop app) |
| API + Pipeline | ✅ Live | DO App Platform |
| Script Generation | ✅ Built | `api/services/llm.py` |
| Image Generation | ✅ Built | `api/services/images.py` |
| Voiceover | ✅ Built | `api/services/voice.py` |
| Video Assembly | ✅ Built | `api/services/video.py` |

---

## Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  CLIENT                                                         │
│  ┌──────────────┐                                               │
│  │ Website Form │ (bom-studios.vercel.app/starten)              │
│  └──────┬───────┘                                               │
└─────────┼───────────────────────────────────────────────────────┘
          │ POST /api/webhooks/tally
          ▼
┌─────────────────────────────────────────────────────────────────┐
│  API (FastAPI on DO App Platform)                               │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ 1. Parse &   │───▶│ 2. Generate  │───▶│ 3. Generate  │      │
│  │    Validate  │    │    Script    │    │ Image Prompts│      │
│  └──────────────┘    │   (Claude)   │    │   (Claude)   │      │
│                      └──────────────┘    └──────────────┘      │
│                                                 │               │
│                      ┌──────────────────────────┴─────┐        │
│                      ▼                                ▼        │
│              ┌──────────────┐                ┌──────────────┐  │
│              │ 4. Generate  │                │ 5. Generate  │  │
│              │    Images    │                │   Voiceover  │  │
│              │ (Replicate)  │                │ (ElevenLabs) │  │
│              └──────┬───────┘                └──────┬───────┘  │
│                     │  (parallel)                  │          │
│                     └───────────────┬───────────────┘          │
│                                     ▼                          │
│                            ┌──────────────┐                    │
│                            │ 6. Assemble  │                    │
│                            │    Video     │                    │
│                            │   (FFmpeg)   │                    │
│                            └──────┬───────┘                    │
│                                   │                            │
└───────────────────────────────────┼────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│  REVIEW QUEUE                                                   │
│  ┌──────────────┐                                               │
│  │ Draft Video  │ → Jeroen reviews in Engine                    │
│  └──────┬───────┘                                               │
│         │ approve / request changes                             │
│         ▼                                                       │
│  ┌──────────────┐                                               │
│  │ Client Portal│ → Client approves                             │
│  └──────┬───────┘                                               │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────┐                                               │
│  │  Delivered   │ → Google Drive + notification                 │
│  └──────────────┘                                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Intake Form Fields

The website form (`/starten`) collects:

| Field | Key | Type | Required |
|-------|-----|------|----------|
| Business Name | `business_name` | text | Yes |
| Email | `email` | email | Yes |
| Website & Social Links | `links` | textarea | No |
| What do you sell/offer? | `what_they_sell` | textarea | Yes |
| Who is your customer? | `target_customer` | textarea | Yes |
| What makes you different? | `what_makes_different` | textarea | Yes |
| Language | `language` | select | Yes |
| Video Style | `video_style` | radio | Yes |
| Video Length | `video_length` | radio | Yes |
| Specific Topic | `topic` | textarea | No |
| Reference Videos | `reference_videos` | textarea | No |
| Anything Else | `notes` | textarea | No |

### Language Options
- `nl` — Dutch
- `en` — English
- `nl+en` — Dutch + English
- `other` — Custom (free text)

### Video Style Options
- `presenter` — Presenter to Camera (trust, directness, services)
- `product` — Product Showcase (fast cuts, e-commerce)
- `animated` — Animated Explainer (apps, tools, SaaS)
- `voiceover` — Voiceover + B-roll (professional, no on-camera)
- `hybrid` — Mix formats

### Video Length Options
- `6s` — Bumper/teaser (2-3 scenes)
- `15s` — Standard social (3-4 scenes)
- `30s` — Extended story (5-7 scenes)

---

## API Endpoints

### Webhook (Form Submission)
```
POST /api/webhooks/tally
```

Accepts Tally-compatible payload:
```json
{
  "eventId": "web-1701234567890",
  "eventType": "FORM_RESPONSE",
  "createdAt": "2024-12-01T20:00:00.000Z",
  "data": {
    "fields": [
      {"key": "business_name", "label": "Business Name", "value": "..."},
      {"key": "email", "label": "Email", "value": "..."},
      {"key": "video_style", "label": "Video Style", "value": "presenter"},
      ...
    ]
  }
}
```

### Other Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/clients` | List clients |
| POST | `/api/clients` | Create client |
| GET | `/api/projects` | List projects |
| GET | `/api/videos` | List videos |
| POST | `/api/videos/{id}/approve` | Approve video |
| POST | `/api/auth/magic-link` | Send login link |
| GET | `/api/auth/verify` | Exchange token for JWT |

---

## Pipeline Services

### 1. Script Generation (`services/llm.py`)

Uses Claude API to generate structured scripts:

```python
async def generate_script(
    business_name: str,
    what_they_sell: str,
    target_customer: str,
    what_makes_different: str,
    tone: str = "friendly",
    language: str = "EN",
    topic: str = None,
    video_style: str = "voiceover",
    video_length: str = "15s",
) -> dict
```

Output:
```json
{
  "hook": "Opening line (2-3 seconds)",
  "scenes": [
    {"text": "Scene 1 narration", "duration": 5},
    {"text": "Scene 2 narration", "duration": 6}
  ],
  "cta": "Closing call to action",
  "total_duration": 35
}
```

### 2. Image Prompt Generation (`services/llm.py`)

```python
async def generate_image_prompts(
    script: dict,
    industry: str,
) -> list[dict]
```

### 3. Image Generation (`services/images.py`)

Uses Replicate (Flux) for image generation:

```python
async def generate_images_parallel(
    prompts: list[str],
    aspect_ratio: str = "9:16",
) -> list[str]
```

Runs all prompts in parallel for speed.

### 4. Voiceover Generation (`services/voice.py`)

Uses ElevenLabs:

```python
async def generate_voiceover(
    text: str,
    language: str = "EN",
    voice_id: str = None,
) -> bytes
```

### 5. Video Assembly (`services/video.py`)

Uses FFmpeg:

```python
async def assemble_video_simple(
    image_urls: list[str],
    audio_url: str,
    output_format: str = "vertical",
) -> Path
```

---

## Cost Estimates

| Step | Cost per Video | Notes |
|------|----------------|-------|
| Script (Claude) | ~$0.01 | Sonnet model |
| Image Prompts (Claude) | ~$0.01 | Sonnet model |
| Images (Replicate) | ~$0.02 | 5-7 images × $0.003 |
| Voiceover (ElevenLabs) | ~$0.12 | ~400 chars |
| **Total** | **~$0.16-0.20** | Without avatar |

At 160 videos/month (8 × 20 clients) = ~$32/month in API costs.

---

## Environment Variables

```bash
# Database
DATABASE_URL=sqlite+aiosqlite:///./data/bom.db  # Demo
# DATABASE_URL=postgresql+asyncpg://...          # Production

# Auth
JWT_SECRET=your-secret-here  # openssl rand -hex 32

# AI Services (optional for full pipeline)
ANTHROPIC_API_KEY=sk-ant-...
REPLICATE_API_TOKEN=r8_...
ELEVENLABS_API_KEY=...

# Debug
DEBUG=true  # Logs magic links to console
```

---

## Deployment

### Current: DigitalOcean App Platform (Demo)

1. Connect GitHub repo
2. Source directory: `/api`
3. Add environment variables
4. Deploy

### Future: Coolify (Production)

Self-hosted on VPS for lower cost at scale.

---

## Webhook Configuration

In Vercel (website), set:
```
NEXT_PUBLIC_INTAKE_WEBHOOK_URL=https://your-api.ondigitalocean.app/api/webhooks/tally
```

---

## What's Automated vs Manual

| Task | Before | After |
|------|--------|-------|
| Receive intake | Manual email | Auto-form |
| Write script | Jeroen writes | AI generates |
| Generate images | Manual creation | AI generates |
| Record voiceover | Manual recording | AI generates |
| Assemble video | Manual editing | Auto FFmpeg |
| Create draft | Manual upload | Auto pipeline |
| **Review & approve** | **Jeroen** | **Jeroen** |

---

## Limitations

1. **Quality variance** — Scripts may need 20-30% manual rewrite
2. **Image coherence** — Style consistency across scenes not guaranteed
3. **Audio sync** — Auto-timing is approximate
4. **No avatar** — HeyGen too expensive for automation, keep manual

---

## Next Steps

1. [x] Connect website form to deployed API
2. [ ] Add API keys for AI services (DO dashboard)
3. [x] Build review queue in Engine
4. [x] Client approval flow in Portal
5. [ ] Google Drive delivery
6. [ ] Email notifications (Resend)

---

*Updated: December 2025*
