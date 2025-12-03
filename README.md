# BOM Studios

Internal video production platform for a Dutch social media agency. Automates video creation from client intake to delivery.

## Quick Links

| Resource | Description |
|----------|-------------|
| **[Setup Guide](docs/video-api-user-guide.md)** | Complete guide to all APIs, services, and getting started |
| [CLAUDE.md](CLAUDE.md) | Technical reference for the codebase |

## Architecture

```
Client intake form → AI script → AI images → AI voice → Video assembly → Delivery
```

**Three applications:**

| App | Tech | Purpose |
|-----|------|---------|
| `api/` | FastAPI | Backend, webhooks, video assembly |
| `portal/` | Next.js | Client login, approvals, downloads |
| `engine/` | Flet | Internal desktop tool |

## Getting Started

### 1. Get API Keys (15 min)

You need 3 API keys to generate videos:

| Service | Get Key At | Env Variable |
|---------|------------|--------------|
| Claude | [console.anthropic.com](https://console.anthropic.com) | `ANTHROPIC_API_KEY` |
| Replicate | [replicate.com](https://replicate.com) | `REPLICATE_API_TOKEN` |
| ElevenLabs | [elevenlabs.io](https://elevenlabs.io) | `ELEVENLABS_API_KEY` |

### 2. Install FFmpeg

```bash
# Mac
brew install ffmpeg

# Linux
sudo apt install ffmpeg

# Windows
choco install ffmpeg
```

### 3. Configure Environment

Create `api/.env`:

```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
REPLICATE_API_TOKEN=r8_...
ELEVENLABS_API_KEY=...
JWT_SECRET=random-string-here
DATABASE_URL=sqlite+aiosqlite:///./data/bom.db
```

### 4. Run the API

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 5. Generate a Test Video

```bash
curl -X POST http://localhost:8000/api/videos/test-pipeline \
  -H "Content-Type: application/json" \
  -d '{"business_name": "Test", "what_they_sell": "Coffee", "language": "nl", "video_length": "15s"}'
```

## Documentation

- **[docs/video-api-user-guide.md](docs/video-api-user-guide.md)** - Full setup guide with:
  - AI model tiers explained (Opus vs Sonnet vs Haiku)
  - All third-party APIs and alternatives
  - Infrastructure services (n8n, DigitalOcean, etc.)
  - Cost calculator
  - Step-by-step setup

## Cost Per Video

| Setup | Cost |
|-------|------|
| Current (Claude + Replicate + ElevenLabs) | ~€0.16 |
| Budget (Gemini + fal.ai + Polly) | ~€0.03 |

## Project Status

- [x] API with video pipeline
- [x] Script & image generation
- [x] Voice generation
- [x] Video assembly (FFmpeg)
- [x] Google Drive delivery
- [ ] n8n automation (Phase 2.5)
- [ ] HeyGen avatars (Phase 2b)
- [ ] Stripe payments (Phase 4)
