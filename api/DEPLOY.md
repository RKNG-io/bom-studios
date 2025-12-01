# BOM Studios API Deployment

## Current: DigitalOcean App Platform (Demo)

For quick demo/MVP deployment.

### Deploy Steps

1. Push to GitHub
2. Go to [DO App Platform](https://cloud.digitalocean.com/apps)
3. Create App → GitHub → Select `bom-studios` repo
4. Set source directory to `/api`
5. Add environment variables:
   - `DATABASE_URL` (use DO Managed PostgreSQL or SQLite for demo)
   - `JWT_SECRET` (generate with `openssl rand -hex 32`)
   - `ANTHROPIC_API_KEY` (for script generation)
   - `REPLICATE_API_TOKEN` (for image generation)
   - `ELEVENLABS_API_KEY` (for voiceover)
   - `DEBUG=false`
6. Deploy

### Webhook URL

Once deployed, set in Vercel:
```
NEXT_PUBLIC_INTAKE_WEBHOOK_URL=https://your-app.ondigitalocean.app/api/webhooks/tally
```

---

## Future: Coolify (Production)

For production, migrate to self-hosted Coolify for:
- Lower cost at scale
- Full control
- No vendor lock-in

### Coolify Setup

1. Provision VPS (DigitalOcean Droplet, Hetzner, etc.)
2. Install Coolify: `curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash`
3. Add PostgreSQL service
4. Connect GitHub repo
5. Set environment variables
6. Deploy

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| DATABASE_URL | Yes | PostgreSQL connection string |
| JWT_SECRET | Yes | Secret for JWT tokens |
| ANTHROPIC_API_KEY | No* | Claude API for script generation |
| REPLICATE_API_TOKEN | No* | Replicate API for images |
| ELEVENLABS_API_KEY | No* | ElevenLabs API for voiceover |
| DEBUG | No | Enable debug mode (magic link logging) |

*Required for full video pipeline to work
