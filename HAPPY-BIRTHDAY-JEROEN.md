# Happy Birthday, Jeroen! 🎂

---

## Your Video Empire Awaits

This is **BOM Studios** — an automated video production pipeline built just for you. Client submits a form, AI generates the script, images, and voiceover, then assembles a draft video. You review, tweak, deliver. Done.

No more hours of manual work per video. Now it's minutes.

---

## What's Been Built

### 🌐 Website
**Live at:** https://bom-studios.vercel.app

| Feature | Status |
|---------|--------|
| Landing page (EN/NL) | ✅ Live |
| Pricing packages | ✅ Live |
| How it works | ✅ Live |
| Intake form at `/starten` | ✅ Live |
| Language toggle | ✅ Live |
| Mobile responsive | ✅ Live |

**Tech:** Next.js 14, Tailwind CSS, Vercel hosting

---

### ⚙️ API + Pipeline
**Live at:** DigitalOcean App Platform

| Component | Status | What it does |
|-----------|--------|--------------|
| Client management | ✅ Built | Stores client info from intake |
| Project tracking | ✅ Built | Links clients to their videos |
| Script generation | ✅ Built | Claude AI writes the script |
| Image prompts | ✅ Built | Claude creates Flux prompts |
| Image generation | ✅ Built | Replicate/Flux makes images |
| Voiceover | ✅ Built | ElevenLabs generates audio |
| Video assembly | ✅ Built | FFmpeg stitches it together |
| Magic link auth | ✅ Built | Passwordless client login |

**Tech:** FastAPI, Python 3.11, SQLAlchemy, async everywhere

---

### 🎬 Video Specs Supported

**Styles:**
- `presenter` — Direct to camera, trust-building
- `product` — Fast cuts, e-commerce vibes
- `animated` — Clean explainer style
- `voiceover` — Professional B-roll + VO
- `hybrid` — Mix of everything

**Lengths:**
- `6s` — Bumper/teaser (2-3 scenes)
- `15s` — Standard social (3-4 scenes)
- `30s` — Extended story (5-7 scenes)

---

## What's Left To Do

### 🔴 Priority 1: Connect the Pieces

| Task | Effort | Notes |
|------|--------|-------|
| Add API keys to DO | 5 min | ANTHROPIC_API_KEY, REPLICATE_API_TOKEN, ELEVENLABS_API_KEY |
| Connect website to API | 5 min | Set NEXT_PUBLIC_INTAKE_WEBHOOK_URL in Vercel |
| Test end-to-end | 15 min | Submit form, check API logs |

### 🟡 Priority 2: Review & Delivery

| Task | Effort | Notes |
|------|--------|-------|
| Review queue UI | 2-3 days | Where you approve/reject drafts |
| Client portal | 2-3 days | Where clients view & approve |
| Google Drive delivery | 1 day | Auto-upload approved videos |
| Email notifications | 1 day | "Your video is ready" emails |

### 🟢 Priority 3: Nice to Have

| Task | Notes |
|------|-------|
| Stripe integration | Auto-billing for packages |
| Usage dashboard | Track videos/client/month |
| Custom domains | bom-studios.nl |
| HeyGen avatars | Too expensive for automation, keep manual |

---

## Your Credentials & Access

### Vercel (Website)
```
Project: bom-studios
URL: https://bom-studios.vercel.app
Dashboard: https://vercel.com
```

### DigitalOcean (API)
```
App: bom-studios-api
Dashboard: https://cloud.digitalocean.com/apps
```

### GitHub
```
Repo: https://github.com/RKNG-io/bom-studios
```

---

## Environment Variables Needed

### In DigitalOcean (API)
```bash
# Required for AI pipeline
ANTHROPIC_API_KEY=sk-ant-...          # Claude for scripts
REPLICATE_API_TOKEN=r8_...            # Flux for images
ELEVENLABS_API_KEY=...                # Voice generation

# Security (generate with: openssl rand -hex 32)
JWT_SECRET=your-secret-here
MAGIC_LINK_SECRET=another-secret

# Optional
DEBUG=false
```

### In Vercel (Website)
```bash
NEXT_PUBLIC_INTAKE_WEBHOOK_URL=https://your-do-app.ondigitalocean.app/api/webhooks/tally
```

---

## How the Pipeline Works

```
┌─────────────────┐
│  Client fills   │
│  intake form    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  API receives   │
│  webhook POST   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│  Claude writes  │────▶│  Claude creates │
│  the script     │     │  image prompts  │
└─────────────────┘     └────────┬────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              ▼                                     ▼
    ┌─────────────────┐                   ┌─────────────────┐
    │  Replicate/Flux │                   │  ElevenLabs     │
    │  generates imgs │                   │  generates voice│
    └────────┬────────┘                   └────────┬────────┘
             │                                     │
             └──────────────┬──────────────────────┘
                            ▼
                  ┌─────────────────┐
                  │  FFmpeg stitches│
                  │  draft video    │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  YOU review     │
                  │  and approve    │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Client gets    │
                  │  final video    │
                  └─────────────────┘
```

---

## Cost Estimates (Per Video)

| Step | Cost |
|------|------|
| Script (Claude) | ~€0.01 |
| Image prompts (Claude) | ~€0.01 |
| Images (Replicate) | ~€0.02 |
| Voiceover (ElevenLabs) | ~€0.12 |
| **Total** | **~€0.16** |

At 160 videos/month (8 per client × 20 clients) = **~€26/month** in API costs.

---

## Quick Commands

### Test API Health
```bash
curl https://your-do-app.ondigitalocean.app/health
```

### View API Docs
```
https://your-do-app.ondigitalocean.app/docs
```

### Local Development
```bash
# Website
cd website && npm run dev

# API
cd api && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## The Vision

**Before:** Hours per video. Manual everything. Bottleneck = you.

**After:** Minutes per video. AI does the grunt work. Bottleneck = review only.

Scale to 20+ clients. Deliver 160+ videos/month. Sleep at night.

---

## One Last Thing

This was built with love (and a lot of Claude). The foundation is solid. The automation is real. Now go make some videos.

**Happy Birthday, Jeroen. Go build your empire.** 🚀

---

*Built by Liz with Claude Code — December 2024*
