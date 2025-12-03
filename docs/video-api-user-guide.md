# Video Generation API User Guide

**For:** Jeroen
**Last Updated:** December 2024

This guide covers all third-party APIs and services needed for BOM Studios video generation, including setup instructions and alternative providers you may wish to test.

---

## Table of Contents

1. [Overview](#overview)
2. [Required APIs](#required-apis)
   - [Claude API (Script Generation)](#1-claude-api-anthropic---script-generation)
   - [Replicate (Image Generation)](#2-replicate---image-generation)
   - [ElevenLabs (Voice Generation)](#3-elevenlabs---voice-generation)
   - [FFmpeg (Video Assembly)](#4-ffmpeg---video-assembly)
3. [Optional APIs](#optional-apis)
   - [HeyGen (Avatar Videos)](#5-heygen---avatar-videos)
   - [Google Drive (Delivery)](#6-google-drive---file-delivery)
4. [Alternative Providers](#alternative-providers)
5. [Cost Comparison](#cost-comparison)
6. [Quick Setup Checklist](#quick-setup-checklist)

---

## Overview

The BOM Studios video pipeline uses several APIs to automate video creation:

```
Script (Claude) → Images (Replicate) → Voice (ElevenLabs) → Assembly (FFmpeg)
```

**Estimated time per video:** 8-14 minutes
**Estimated cost per video:** €0.15-0.20

---

## Required APIs

### 1. Claude API (Anthropic) - Script Generation

**What it does:** Generates video scripts and image prompts using AI

**Current model:** `claude-sonnet-4-20250514`

#### Setup

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Create an account and add billing
3. Generate an API key under "API Keys"
4. Add to your `.env` file:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
   ```

#### Pricing

| Usage | Cost |
|-------|------|
| Input tokens | $3.00 / 1M tokens |
| Output tokens | $15.00 / 1M tokens |
| **Per video (avg)** | **~€0.02** |

#### How We Use It

- **Script generation:** Creates structured scripts with hook, scenes, and CTA
- **Image prompts:** Converts script scenes into visual descriptions for image generation
- **Supports:** Dutch/English, multiple tones (friendly, professional, bold), various video lengths (6s, 15s, 30s)

#### Alternatives to Test

| Provider | Model | Pros | Cons | Pricing |
|----------|-------|------|------|---------|
| **OpenAI** | GPT-4o | Widely used, good Dutch | Slightly less creative | $5-15/1M tokens |
| **Google** | Gemini 1.5 Pro | Cheap, large context | Weaker creative writing | $1.25-5/1M tokens |
| **Mistral** | Mistral Large | EU-based, GDPR friendly | Smaller ecosystem | $2-6/1M tokens |
| **Groq** | Llama 3.1 70B | Extremely fast, cheap | Open model limitations | ~$0.60/1M tokens |

**Recommendation:** Stick with Claude for creative scripts. Test Gemini for cost reduction if budget is a concern.

---

### 2. Replicate - Image Generation

**What it does:** Generates AI images for each video scene

**Current model:** `black-forest-labs/flux-schnell` (fast, high quality)

#### Setup

1. Go to [replicate.com](https://replicate.com)
2. Sign up with GitHub
3. Go to Account → API Tokens
4. Add to your `.env` file:
   ```
   REPLICATE_API_TOKEN=r8_xxxxx
   ```

#### Pricing

| Usage | Cost |
|-------|------|
| Flux Schnell | ~$0.003 per image |
| **Per video (5-7 images)** | **~€0.02** |

#### How We Use It

- **Aspect ratio:** 9:16 (vertical for Reels/TikTok/Shorts)
- **Parallel generation:** All images generate simultaneously
- **Timeout:** 60 seconds max per image

#### Alternatives to Test

| Provider | Model | Pros | Cons | Pricing |
|----------|-------|------|------|---------|
| **Replicate** | Flux Pro | Higher quality | Slower, more expensive | $0.05/image |
| **Replicate** | Flux Dev | Middle ground | Moderate speed | $0.025/image |
| **Stability AI** | Stable Diffusion 3 | Direct API, consistent | Less stylized | $0.04-0.08/image |
| **Midjourney** | MJ v6.1 | Best aesthetics | No API (workarounds exist) | $8-30/month |
| **Leonardo AI** | Various | Good UI, API available | Smaller community | $0.02-0.04/image |
| **Ideogram** | Ideogram 2.0 | Best text rendering | Limited styles | $0.02-0.04/image |
| **fal.ai** | Flux variants | Very fast, cheap | Less known | $0.002-0.01/image |

**Recommendation:**
- **Budget:** Try fal.ai (same Flux models, cheaper)
- **Quality:** Test Flux Pro for important clients
- **Text in images:** Use Ideogram when text accuracy matters

---

### 3. ElevenLabs - Voice Generation

**What it does:** Converts script text to realistic voiceover audio

**Current model:** `eleven_multilingual_v2`

#### Setup

1. Go to [elevenlabs.io](https://elevenlabs.io)
2. Create account and choose a plan
3. Go to Profile → API Key
4. Add to your `.env` file:
   ```
   ELEVENLABS_API_KEY=xxxxx
   ```

#### Pricing

| Plan | Characters/month | Cost |
|------|------------------|------|
| Free | 10,000 | €0 |
| Starter | 30,000 | €5/month |
| Creator | 100,000 | €22/month |
| Pro | 500,000 | €99/month |
| **Per video (~400 chars)** | | **~€0.12** |

#### Pre-configured Voices

| Voice | ID | Language |
|-------|-----|----------|
| Adam (Male) | `pNInz6obpgDQGcFmaJgB` | Dutch/English |
| Rachel (Female) | `21m00Tcm4TlvDq8ikWAM` | Dutch/English |

#### How We Use It

- **Output format:** MP3
- **Voice settings:** Stability 0.5, Similarity 0.75
- **Languages:** Dutch and English supported

#### Alternatives to Test

| Provider | Pros | Cons | Pricing |
|----------|------|------|---------|
| **Play.ht** | Great Dutch, voice cloning | Newer platform | $31-99/month |
| **Murf.ai** | Studio UI, good accents | API less flexible | $23-79/month |
| **WellSaid Labs** | Enterprise quality | US-focused | $49-99/month |
| **Amazon Polly** | Cheap, reliable | Less natural | $4/1M chars |
| **Google Cloud TTS** | Very cheap, many languages | Robotic feel | $4-16/1M chars |
| **Azure TTS** | Good Dutch, neural voices | Complex setup | $15/1M chars |
| **Resemble AI** | Voice cloning | Complex | $0.06/second |

**Recommendation:**
- **Budget:** Amazon Polly or Google Cloud TTS (10-20x cheaper)
- **Quality (Dutch):** Stick with ElevenLabs or try Play.ht
- **Volume:** Azure TTS offers good Dutch at scale

---

### 4. FFmpeg - Video Assembly

**What it does:** Combines images, voiceover, and music into final video

**Cost:** Free (local processing)

#### Setup

Install FFmpeg on your system:

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows (via Chocolatey)
choco install ffmpeg

# Verify installation
ffmpeg -version
```

#### Features We Use

- **Ken Burns effect:** Subtle zoom/pan on images
- **Audio mixing:** Voiceover + background music
- **Output formats:** Vertical (9:16), Square (1:1), Horizontal (16:9)
- **Codecs:** H.264 video, AAC audio

#### Alternatives

| Tool | Pros | Cons | Cost |
|------|------|------|------|
| **MoviePy** | Python library, simpler | Slower, less features | Free |
| **Shotstack** | Cloud API, no FFmpeg needed | Monthly cost | $25-100/month |
| **Creatomate** | Template-based, API | Monthly cost | $49-199/month |
| **Bannerbear** | Video API | Limited features | $49-199/month |
| **JSON2Video** | Simple JSON input | Basic output | $20-80/month |

**Recommendation:** Stick with FFmpeg (free, full control). Consider Shotstack/Creatomate only if you need cloud rendering for scale.

---

## Optional APIs

### 5. HeyGen - Avatar Videos

**Status:** Planned for Phase 2b

**What it does:** Creates realistic AI avatars speaking your script

#### Setup

1. Go to [heygen.com](https://heygen.com)
2. Create business account
3. API access requires paid plan
4. Add to your `.env` file:
   ```
   HEYGEN_API_KEY=xxxxx
   ```

#### Pricing

| Plan | Credits | Cost |
|------|---------|------|
| Creator | 15 credits | $29/month |
| Business | 60 credits | $89/month |
| **Per 1-min video** | | **~€2-5** |

#### Alternatives to Test

| Provider | Pros | Cons | Pricing |
|----------|------|------|---------|
| **D-ID** | Good API, natural motion | Expensive at scale | $0.02-0.05/second |
| **Synthesia** | Best quality | Very expensive | $29-90/video |
| **Tavus** | Personalization focus | Limited avatars | Custom |
| **Runway** | Gen-2 video AI | Different use case | $12-76/month |
| **Pika Labs** | Creative video | Less realistic | Free/$8/month |

**Recommendation:** HeyGen has the best Dutch support. Test D-ID as backup. Synthesia for premium clients.

---

### 6. Google Drive - File Delivery

**What it does:** Stores and shares final videos with clients

#### Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project
3. Enable Google Drive API
4. Create Service Account with Editor role
5. Download JSON credentials
6. Create a shared folder in Drive
7. Share folder with service account email
8. Add to your `.env` file:
   ```
   GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'
   GOOGLE_DRIVE_FOLDER_ID=xxxxx
   ```

#### Pricing

| Storage | Cost |
|---------|------|
| First 15GB | Free |
| Google Workspace | €5.75-17.25/user/month |

#### Alternatives

| Service | Pros | Cons | Pricing |
|---------|------|------|---------|
| **Bunny CDN** | Fast, cheap, global | Video add-on needed | $0.01/GB stored |
| **Backblaze B2** | Very cheap storage | No viewer interface | $0.005/GB stored |
| **AWS S3** | Reliable, scalable | Complex, adds up | $0.023/GB stored |
| **Cloudflare R2** | No egress fees | Newer | $0.015/GB stored |
| **Vimeo** | Pro video hosting | Expensive | $12-65/month |
| **Mux** | Developer-friendly | Pay per minute | $0.002/min watched |

**Recommendation:** Keep Google Drive for simplicity. Consider Bunny CDN or Mux for scale/embedding.

---

## Alternative Providers

### All-in-One Video APIs

If you want to simplify the stack, these services combine multiple steps:

| Service | What it replaces | Pros | Cons | Pricing |
|---------|-----------------|------|------|---------|
| **Creatomate** | FFmpeg + rendering | Templates, API | Limited AI | $49-199/month |
| **Shotstack** | FFmpeg + rendering | Cloud scale | No AI generation | $25-100/month |
| **Runway** | Images + video | AI-native | Different style | $12-76/month |
| **Lumen5** | Script → video | Automated | Template-based | $19-149/month |
| **Pictory** | Script → video | Easy | Less control | $23-119/month |

---

## Cost Comparison

### Current Stack (Per Video)

| Service | Cost |
|---------|------|
| Claude (script + prompts) | €0.02 |
| Replicate (images) | €0.02 |
| ElevenLabs (voice) | €0.12 |
| FFmpeg | Free |
| **Total** | **~€0.16** |

### Budget Alternative Stack

| Service | Cost |
|---------|------|
| Gemini 1.5 Pro (script) | €0.005 |
| fal.ai (images) | €0.01 |
| Amazon Polly (voice) | €0.01 |
| FFmpeg | Free |
| **Total** | **~€0.025** |

### Premium Stack

| Service | Cost |
|---------|------|
| Claude Opus (script) | €0.08 |
| Flux Pro (images) | €0.35 |
| ElevenLabs (voice) | €0.12 |
| HeyGen (avatar) | €3.00 |
| **Total** | **~€3.55** |

---

## Quick Setup Checklist

### Minimum Required (MVP)

- [ ] **Anthropic API Key** - [console.anthropic.com](https://console.anthropic.com)
- [ ] **Replicate Token** - [replicate.com](https://replicate.com)
- [ ] **ElevenLabs Key** - [elevenlabs.io](https://elevenlabs.io)
- [ ] **FFmpeg installed** - `brew install ffmpeg`

### Full Production

- [ ] All MVP requirements
- [ ] **Google Drive** service account configured
- [ ] **HeyGen API Key** (for avatar videos)
- [ ] **Resend API Key** (for email notifications)

### Environment File Template

```bash
# Required for video generation
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
REPLICATE_API_TOKEN=r8_xxxxx
ELEVENLABS_API_KEY=xxxxx

# Optional - Avatar videos
HEYGEN_API_KEY=xxxxx

# Optional - File delivery
GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'
GOOGLE_DRIVE_FOLDER_ID=xxxxx

# Optional - Notifications
RESEND_API_KEY=re_xxxxx
```

---

## Testing New Providers

When testing alternatives:

1. **Start small** - Test with 1-2 videos first
2. **Compare quality** - Save outputs side by side
3. **Measure latency** - Some cheap options are slow
4. **Check Dutch support** - Many US services lack good Dutch
5. **Review rate limits** - Free tiers often throttle heavily
6. **Calculate true cost** - Include overage charges

---

## Questions?

Check the main documentation at `/docs/` or ask in Slack.
