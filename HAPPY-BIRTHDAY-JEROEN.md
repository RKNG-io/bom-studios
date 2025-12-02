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
| Landing page (EN/NL) | Done |
| Pricing packages | Done |
| How it works | Done |
| Intake form at `/starten` | Done |
| Client portal at `/login` | Done |
| Dashboard with projects/videos | Done |
| Magic link authentication | Done |
| Language toggle | Done |
| Mobile responsive | Done |

**Tech:** Next.js 14, Tailwind CSS, Vercel hosting

---

### ⚙️ API + Pipeline
**Live at:** DigitalOcean App Platform

| Component | Status | What it does |
|-----------|--------|--------------|
| Client management | Done | Stores client info from intake |
| Project tracking | Done | Links clients to their videos |
| Script generation | Done | Claude AI writes the script |
| Image prompts | Done | Claude creates Flux prompts |
| Image generation | Done | Replicate/Flux makes images |
| Voiceover | Done | ElevenLabs generates audio |
| Video assembly | Done | FFmpeg stitches it together |
| Magic link auth | Done | Passwordless client login |

**Tech:** FastAPI, Python 3.11, SQLAlchemy, async everywhere

---

### 🖥️ Engine (Your Review Tool)
**Location:** `/engine`

| Feature | Status |
|---------|--------|
| Dashboard with stats | Done + API connected |
| Projects list | Done + API connected |
| Video library with filters | Done + API connected |
| Create video wizard | Done |
| Settings page | Done |
| BOM Studios theme | Done |

**Tech:** Flet (Python desktop app), runs on your Mac

**API Connected:** The Engine now fetches real data from the API!

**Preview:** [See screenshots of the Engine](engine/ENGINE-PREVIEW.md)

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
| Update DigitalOcean billing | 5 min | Add your payment method at cloud.digitalocean.com/account/billing |
| Update Google Cloud billing | 5 min | Add payment method at console.cloud.google.com/billing |
| Test end-to-end | 15 min | Submit form, check API logs |

### 🟡 Priority 2: Review & Delivery

| Task | Effort | Notes |
|------|--------|-------|
| Client portal | Done | `/login` → `/dashboard` |
| Engine (review queue) | Done | Flet desktop app in `/engine` |
| Google Drive delivery | Ready | See `/docs/GOOGLE-DRIVE-SETUP.md` to configure |
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

### BOM Studios Gmail (Temporary)
```
Email: jeroen.bomstudios@gmail.com
Password: [Ask Liz for the password]
```
*This is your business account for Google Cloud, Drive, etc. Use it until you buy a domain and set up proper email (e.g., jeroen@bom-studios.nl)*

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

### Google Cloud (Drive API)
```
Console: https://console.cloud.google.com
Login: jeroen.bomstudios@gmail.com
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

### Install the Engine (Your Desktop App)

This is your personal review tool. Runs on your Mac.

```bash
# 1. Clone the repo (if you haven't already)
git clone https://github.com/RKNG-io/bom-studios.git
cd bom-studios/engine

# 2. Set up Python environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -e .

# 4. Run the app
python app.py
```

A window will open with your dashboard. That's it!

**Shortcut for next time:**
```bash
cd bom-studios/engine
source .venv/bin/activate
python app.py
```

### Local Development (Website & API)
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

This was built with care. The foundation is solid. The automation is real. Now go make some videos.

**Happy Birthday, Jeroen. Go build your empire.** 🚀

---

*Built by Margaret — 2 December 2025*
