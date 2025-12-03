# BOM Studios - Complete Setup Guide

**For:** Jeroen
**Last Updated:** December 2024

A beginner-friendly guide to all the services you need to connect, what they do, and how to get from zero to generating test videos.

---

## Table of Contents

1. [The Big Picture](#the-big-picture)
2. [Understanding AI Models](#understanding-ai-models)
3. [Video Generation APIs](#video-generation-apis)
4. [Infrastructure Services](#infrastructure-services)
5. [What You Need Right Now](#what-you-need-right-now)
6. [Step-by-Step Setup](#step-by-step-setup)
7. [Testing Your First Video](#testing-your-first-video)
8. [Cost Calculator](#cost-calculator)

---

## The Big Picture

### What BOM Studios Does

```
Client fills form → AI writes script → AI makes images → AI generates voice → Video assembled
```

### All The Services (Overview)

| Category | Service | What It Does | Need Now? |
|----------|---------|--------------|-----------|
| **AI Brain** | Claude/Gemini/GPT | Writes scripts | Yes |
| **Images** | Replicate/fal.ai | Creates visuals | Yes |
| **Voice** | ElevenLabs | Speaks the script | Yes |
| **Video** | FFmpeg | Combines everything | Yes (free) |
| **Forms** | Tally | Client intake | Later |
| **Automation** | n8n | Connects everything | Later |
| **Hosting** | DigitalOcean | Runs the API | Later |
| **Website** | Vercel | Hosts the website | Later |
| **Storage** | Google Drive | Delivers videos | Later |
| **Email** | Resend | Sends notifications | Later |
| **Payments** | Stripe | Takes payments | Much later |

---

## Understanding AI Models

### The Restaurant Analogy

Think of AI models like restaurants:

| Tier | Restaurant | AI Examples | Best For |
|------|------------|-------------|----------|
| **Premium** | Michelin star | Claude Opus, GPT-4, Gemini Ultra | Complex creative work |
| **Standard** | Nice bistro | Claude Sonnet, GPT-4o, Gemini Pro | Daily production work |
| **Budget** | Fast food | Claude Haiku, GPT-4o-mini, Gemini Flash | Simple quick tasks |

**The key insight:** More expensive doesn't always mean better for YOUR task. A Michelin chef is overkill for making a sandwich.

---

### Claude (Anthropic) - What We Use

Anthropic makes Claude. Here are the model tiers:

| Model | Speed | Quality | Price | Best For |
|-------|-------|---------|-------|----------|
| **Opus** | Slow | Exceptional | €15/1M tokens | Complex reasoning, research |
| **Sonnet** | Medium | Very good | €3/1M tokens | Creative writing, scripts |
| **Haiku** | Fast | Good | €0.25/1M tokens | Simple tasks, summaries |

**We use:** Sonnet (best balance for video scripts)

**Tokens explained:** ~750 words = 1,000 tokens. A video script uses ~500-1000 tokens.

#### When to use each:

```
Haiku  → "Summarize this text" or "Fix this grammar"
Sonnet → "Write a creative video script" ← OUR USE CASE
Opus   → "Analyze this complex business problem"
```

---

### OpenAI (GPT) - Alternative

| Model | Speed | Quality | Price | Comparable To |
|-------|-------|---------|-------|---------------|
| **GPT-4** | Slow | Excellent | €30/1M tokens | Claude Opus |
| **GPT-4o** | Medium | Very good | €5/1M tokens | Claude Sonnet |
| **GPT-4o-mini** | Fast | Good | €0.15/1M tokens | Claude Haiku |

**Verdict:** Similar to Claude. GPT is more widely known, Claude often writes more naturally.

---

### Google (Gemini) - Budget Alternative

| Model | Speed | Quality | Price | Comparable To |
|-------|-------|---------|-------|---------------|
| **Gemini 1.5 Pro** | Medium | Very good | €1.25/1M tokens | Claude Sonnet (cheaper!) |
| **Gemini 1.5 Flash** | Very fast | Good | €0.075/1M tokens | Claude Haiku (much cheaper!) |
| **Gemini 2.0 Flash** | Very fast | Better | €0.10/1M tokens | Between Haiku & Sonnet |

**Verdict:** Best value for money. Good Dutch support. Worth testing!

---

### Other Options

| Provider | Model | Why Consider | Price |
|----------|-------|--------------|-------|
| **Mistral** | Large | EU-based (GDPR) | €2/1M tokens |
| **Groq** | Llama 3.1 | Extremely fast | €0.60/1M tokens |
| **DeepSeek** | V3 | Very cheap | €0.14/1M tokens |

---

### How to Choose a Model

Ask yourself:

1. **Is this task creative?** → Use Sonnet/GPT-4o/Gemini Pro
2. **Is this task simple?** → Use Haiku/GPT-4o-mini/Flash
3. **Is this task complex reasoning?** → Use Opus/GPT-4 (rare)
4. **Am I on a tight budget?** → Use Gemini Flash
5. **Do I need EU data residency?** → Use Mistral

**For BOM Studios video scripts:** Start with Claude Sonnet, test Gemini 1.5 Pro as a cheaper alternative.

---

### Quick Model Comparison Table

| Task | Best Choice | Budget Choice |
|------|-------------|---------------|
| Video scripts | Claude Sonnet | Gemini 1.5 Pro |
| Image prompts | Claude Sonnet | Gemini Flash |
| Summaries | Claude Haiku | Gemini Flash |
| Translations | GPT-4o | Gemini Flash |
| Complex analysis | Claude Opus | GPT-4 |

---

## Video Generation APIs

These are the services that actually create the video content.

### 1. Script Generation (LLM)

**What it does:** Writes the video script with hook, scenes, and call-to-action

| Provider | Model | Quality | Cost/Video | Notes |
|----------|-------|---------|------------|-------|
| **Anthropic** | Claude Sonnet | Excellent | €0.02 | Best creative writing |
| **Google** | Gemini 1.5 Pro | Very good | €0.005 | 4x cheaper, good Dutch |
| **OpenAI** | GPT-4o | Very good | €0.02 | Most popular |
| **Groq** | Llama 3.1 70B | Good | €0.002 | 10x cheaper, fast |

**Current:** Claude Sonnet
**Test:** Gemini 1.5 Pro (same quality, 4x cheaper)

#### Setup (Claude)
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Add payment method
3. Create API key
4. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

#### Setup (Gemini - Alternative)
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Get API key (free tier available!)
3. Add to `.env`: `GOOGLE_API_KEY=...`

---

### 2. Image Generation

**What it does:** Creates the visuals for each scene in the video

| Provider | Model | Quality | Speed | Cost/Image | Notes |
|----------|-------|---------|-------|------------|-------|
| **Replicate** | Flux Schnell | Good | Fast | €0.003 | Current choice |
| **Replicate** | Flux Dev | Better | Medium | €0.025 | Higher quality |
| **Replicate** | Flux Pro | Best | Slow | €0.05 | Premium quality |
| **fal.ai** | Flux Schnell | Good | Very fast | €0.002 | Cheaper! |
| **Stability AI** | SD3 | Good | Medium | €0.04 | Direct API |
| **Leonardo AI** | Various | Good | Medium | €0.02 | Nice UI |
| **Ideogram** | 2.0 | Best text | Medium | €0.03 | Best for text in images |

**Current:** Replicate (Flux Schnell) - ~€0.02 per video (6 images)
**Test:** fal.ai (same model, cheaper)

#### Setup (Replicate)
1. Go to [replicate.com](https://replicate.com)
2. Sign in with GitHub
3. Get API token
4. Add to `.env`: `REPLICATE_API_TOKEN=r8_...`

#### Setup (fal.ai - Alternative)
1. Go to [fal.ai](https://fal.ai)
2. Create account
3. Get API key
4. Add to `.env`: `FAL_KEY=...`

---

### 3. Voice Generation

**What it does:** Converts the script text to spoken audio

| Provider | Quality | Dutch | Cost/Video | Notes |
|----------|---------|-------|------------|-------|
| **ElevenLabs** | Excellent | Great | €0.12 | Best quality |
| **Play.ht** | Very good | Good | €0.08 | Good alternative |
| **Amazon Polly** | Okay | Okay | €0.01 | Very cheap |
| **Google TTS** | Okay | Good | €0.01 | Very cheap |
| **Azure TTS** | Good | Good | €0.02 | Microsoft |

**Current:** ElevenLabs (best Dutch voices)
**Budget test:** Amazon Polly or Google TTS (10x cheaper, lower quality)

#### Setup (ElevenLabs)
1. Go to [elevenlabs.io](https://elevenlabs.io)
2. Create account
3. Pick a plan (Starter €5/month is fine for testing)
4. Get API key from Profile
5. Add to `.env`: `ELEVENLABS_API_KEY=...`

**Pre-configured voices:**
- Dutch Male: Adam (`pNInz6obpgDQGcFmaJgB`)
- Dutch Female: Rachel (`21m00Tcm4TlvDq8ikWAM`)

---

### 4. Video Assembly (FFmpeg)

**What it does:** Combines images + voice + music into final video

**Cost:** FREE (runs on your computer)

#### Setup

```bash
# Mac
brew install ffmpeg

# Ubuntu/Linux
sudo apt install ffmpeg

# Windows
choco install ffmpeg

# Verify
ffmpeg -version
```

**Features we use:**
- Ken Burns effect (subtle zoom on images)
- Audio mixing (voice + background music)
- Multiple formats (9:16 vertical, 1:1 square, 16:9 horizontal)

**No alternatives needed** - FFmpeg is the industry standard and free.

---

### 5. Avatar Videos (Optional - Future)

**What it does:** Creates AI avatars that speak your script

| Provider | Quality | Dutch | Cost/Min | Notes |
|----------|---------|-------|----------|-------|
| **HeyGen** | Excellent | Great | €2-5 | Best Dutch avatars |
| **D-ID** | Very good | Good | €1-2 | Good API |
| **Synthesia** | Best | Good | €5-10 | Premium, expensive |

**Status:** Planned for Phase 2b (not needed yet)

---

## Infrastructure Services

These services run and connect everything together.

### 1. n8n - Automation Platform

**What it does:** Connects all your services together with visual workflows

Think of it like: "When X happens, do Y, then Z"

**Example workflow:**
```
Client submits form → Create project → Generate script → Generate images → Send notification
```

**Why n8n?**
- Self-hosted (your data stays private)
- Visual workflow builder (no code needed)
- Cheaper than Zapier at scale
- Can connect to anything

**Alternatives:**
| Service | Hosting | Cost | Notes |
|---------|---------|------|-------|
| **n8n** | Self-hosted | Free | Our choice |
| **n8n Cloud** | Hosted | €20+/month | Easier setup |
| **Zapier** | Hosted | €20-100/month | Most popular |
| **Make** | Hosted | €9-29/month | Good value |

**Setup:** Later (Phase 2.5) - you don't need this for testing

---

### 2. DigitalOcean (DO) - Cloud Hosting

**What it does:** Runs your API server in the cloud so it's always available

**Think of it like:** Renting a computer that's always on, connected to the internet

**What we host there:**
- FastAPI backend (the brain)
- PostgreSQL database (the memory)

**Alternatives:**
| Service | Type | Cost | Notes |
|---------|------|------|-------|
| **DigitalOcean App Platform** | Managed | €5-12/month | Easy, our choice |
| **DigitalOcean Droplet** | VPS | €4-6/month | More control |
| **Railway** | Managed | €5-20/month | Very easy |
| **Render** | Managed | €0-7/month | Free tier! |
| **Hetzner** | VPS | €3-5/month | Cheapest EU |
| **Coolify** | Self-hosted | VPS cost only | Future plan |

**For testing:** You can run everything locally! No hosting needed yet.

---

### 3. Vercel - Website Hosting

**What it does:** Hosts the website and client portal

**What's hosted there:**
- Landing page (bom-studios.nl)
- Client login portal
- Video approval pages

**Cost:** Free for small projects, €20/month for more

**Alternatives:**
| Service | Cost | Notes |
|---------|------|-------|
| **Vercel** | Free-€20 | Best for Next.js |
| **Netlify** | Free-€19 | Similar to Vercel |
| **Cloudflare Pages** | Free | Very fast |

**Current:** Already set up on Vercel

---

### 4. Tally - Form Builder

**What it does:** Creates the client intake form

**How it works:**
1. Client fills out form on your website
2. Tally sends data to your API (webhook)
3. API starts video generation

**Cost:** Free for basic, €29/month for premium

**Alternatives:**
| Service | Cost | Notes |
|---------|------|-------|
| **Tally** | Free-€29 | Beautiful, simple |
| **Typeform** | €25-83 | More features |
| **Google Forms** | Free | Basic but works |
| **Jotform** | Free-€39 | Many templates |

**Setup:** Create form at [tally.so](https://tally.so), point webhook to your API

---

### 5. Google Drive - File Storage

**What it does:** Stores and shares final videos with clients

**How it works:**
1. Video is generated
2. Uploaded to client's folder in Drive
3. Client gets link to view/download

**Cost:** Free (15GB), or included with Workspace

**Alternatives:**
| Service | Cost | Notes |
|---------|------|-------|
| **Google Drive** | Free | Simple sharing |
| **Dropbox** | €10+/month | Business features |
| **Bunny CDN** | €0.01/GB | Fast streaming |
| **Cloudflare R2** | €0.015/GB | No egress fees |

---

### 6. Resend - Email Service

**What it does:** Sends emails (magic links, notifications)

**Examples:**
- "Click here to log in" (magic link)
- "Your video is ready for review"
- "Video approved, delivering now"

**Cost:** Free (3,000 emails/month), then €20/month

**Alternatives:**
| Service | Free Tier | Paid | Notes |
|---------|-----------|------|-------|
| **Resend** | 3,000/month | €20 | Developer-friendly |
| **SendGrid** | 100/day | €15 | Popular |
| **Postmark** | 100/month | €10 | Transactional focus |
| **Mailgun** | 5,000/month | €35 | Feature-rich |

---

### 7. Stripe - Payments (Future)

**What it does:** Processes client payments

**When needed:** Phase 4 (not now)

**Cost:** 1.4% + €0.25 per transaction (EU cards)

---

## What You Need Right Now

### To Generate Test Videos (Minimum)

You only need **4 things** to start testing:

| Service | Cost | Time to Setup |
|---------|------|---------------|
| Claude API key | ~€5 to start | 5 minutes |
| Replicate token | ~€5 to start | 5 minutes |
| ElevenLabs key | €5/month (Starter) | 5 minutes |
| FFmpeg installed | Free | 2 minutes |

**Total: ~€15 and 20 minutes**

### To Run Full Automation (Later)

| Service | When Needed |
|---------|-------------|
| DigitalOcean hosting | When going live |
| Google Drive setup | When delivering to clients |
| Tally form | When accepting client requests |
| n8n workflows | When automating everything |
| Resend email | When sending notifications |
| Stripe | When charging clients |

---

## Step-by-Step Setup

### Phase 1: Get API Keys (20 minutes)

#### Step 1: Claude (Anthropic)
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up with email
3. Add €5 credit (Settings → Billing)
4. Go to API Keys → Create Key
5. Copy the key starting with `sk-ant-api03-...`

#### Step 2: Replicate
1. Go to [replicate.com](https://replicate.com)
2. Click "Sign in with GitHub"
3. Go to Account → API Tokens
4. Copy the token starting with `r8_...`

#### Step 3: ElevenLabs
1. Go to [elevenlabs.io](https://elevenlabs.io)
2. Sign up
3. Pick "Starter" plan (€5/month)
4. Click profile icon → Profile + API Key
5. Copy the API key

#### Step 4: FFmpeg
```bash
# Mac
brew install ffmpeg

# Linux
sudo apt install ffmpeg

# Windows
choco install ffmpeg
```

### Phase 2: Configure Environment

Create/edit the `.env` file in `/api/`:

```bash
# Minimum for testing
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
REPLICATE_API_TOKEN=r8_your-token-here
ELEVENLABS_API_KEY=your-key-here

# Auth (generate random strings)
JWT_SECRET=generate-a-random-string-here
MAGIC_LINK_SECRET=generate-another-random-string

# Database (local testing)
DATABASE_URL=sqlite+aiosqlite:///./data/bom.db
```

### Phase 3: Run Locally

```bash
# Terminal 1: Start the API
cd api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2: Start the Engine (optional)
cd engine
pip install flet
flet run app.py
```

### Phase 4: Test Video Generation

Use the API directly:

```bash
# Test script generation
curl -X POST http://localhost:8000/api/videos/test-pipeline \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Test Bakkerij",
    "what_they_sell": "Artisan bread and pastries",
    "target_customer": "Health-conscious food lovers",
    "what_makes_different": "Traditional recipes, local ingredients",
    "language": "nl",
    "video_style": "voiceover",
    "video_length": "15s",
    "topic": "New sourdough collection"
  }'
```

---

## Testing Your First Video

### Quick Test Checklist

- [ ] API keys configured in `.env`
- [ ] FFmpeg installed (`ffmpeg -version` works)
- [ ] API running (`http://localhost:8000/health` returns OK)
- [ ] Database created (auto-creates on first run)

### What Happens When You Generate

1. **Script Generation** (30 sec)
   - Claude writes hook, 3-5 scenes, CTA
   - Creates image prompts for each scene

2. **Image Generation** (2-3 min)
   - Replicate generates 5-7 images in parallel
   - Downloads to temp folder

3. **Voice Generation** (30 sec)
   - ElevenLabs converts script to audio
   - Downloads MP3 file

4. **Assembly** (1-2 min)
   - FFmpeg combines everything
   - Adds Ken Burns effect
   - Outputs final MP4

**Total: ~5-8 minutes per video**

---

## Cost Calculator

### Per Video (Current Setup)

| Step | Service | Cost |
|------|---------|------|
| Script | Claude Sonnet | €0.01 |
| Image prompts | Claude Sonnet | €0.01 |
| Images (6x) | Replicate Flux | €0.02 |
| Voiceover | ElevenLabs | €0.12 |
| Assembly | FFmpeg | Free |
| **Total** | | **€0.16** |

### Per Video (Budget Setup)

| Step | Service | Cost |
|------|---------|------|
| Script | Gemini 1.5 Pro | €0.003 |
| Image prompts | Gemini Flash | €0.001 |
| Images (6x) | fal.ai Flux | €0.012 |
| Voiceover | Amazon Polly | €0.01 |
| Assembly | FFmpeg | Free |
| **Total** | | **€0.026** |

### Monthly Projections

| Videos/Month | Current | Budget |
|--------------|---------|--------|
| 10 (testing) | €1.60 | €0.26 |
| 50 | €8 | €1.30 |
| 160 (8 clients) | €26 | €4.20 |
| 500 | €80 | €13 |

---

## Quick Reference Card

### API Keys Needed

```
ANTHROPIC_API_KEY    → console.anthropic.com
REPLICATE_API_TOKEN  → replicate.com
ELEVENLABS_API_KEY   → elevenlabs.io
```

### Model Tiers (Simple)

```
EXPENSIVE & SMART    Opus / GPT-4 / Gemini Ultra
BALANCED (use this)  Sonnet / GPT-4o / Gemini Pro  ←
CHEAP & FAST         Haiku / GPT-4o-mini / Flash
```

### Service Priority

```
NOW     → Claude, Replicate, ElevenLabs, FFmpeg
SOON    → Google Drive, Tally, Resend
LATER   → DigitalOcean, n8n, HeyGen
FUTURE  → Stripe
```

---

## Getting Help

- **Anthropic docs:** [docs.anthropic.com](https://docs.anthropic.com)
- **Replicate docs:** [replicate.com/docs](https://replicate.com/docs)
- **ElevenLabs docs:** [elevenlabs.io/docs](https://elevenlabs.io/docs)
- **n8n docs:** [docs.n8n.io](https://docs.n8n.io)
- **FFmpeg wiki:** [trac.ffmpeg.org](https://trac.ffmpeg.org)

---

## Summary

**To test video generation today:**
1. Get 3 API keys (Claude, Replicate, ElevenLabs) - 15 min
2. Install FFmpeg - 2 min
3. Add keys to `.env` - 2 min
4. Run the API locally - 1 min
5. Generate a test video - 5 min

**Total investment:** ~€15 and 25 minutes

**To go live with clients:** Add Google Drive, Tally forms, hosting, and email. That's Phase 2.

Start simple. Test first. Scale when ready.
