# BOM Studios — Automated Video Pipeline

---

## Overview

Client submits intake form → system produces draft video → Jeroen reviews → client approves → delivered.

**Human touchpoints:** Review and approval only. Everything else automated.

---

## Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  CLIENT                                                         │
│  ┌──────────────┐                                               │
│  │ Intake Form  │ (Tally)                                       │
│  └──────┬───────┘                                               │
└─────────┼───────────────────────────────────────────────────────┘
          │ webhook
          ▼
┌─────────────────────────────────────────────────────────────────┐
│  ORCHESTRATOR (n8n)                                             │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ 1. Parse &   │───▶│ 2. Generate  │───▶│ 3. Generate  │      │
│  │    Validate  │    │    Script    │    │ Image Prompts│      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                 │               │
│                      ┌──────────────────────────┴─────┐        │
│                      ▼                                ▼        │
│              ┌──────────────┐                ┌──────────────┐  │
│              │ 4. Generate  │                │ 5. Generate  │  │
│              │    Images    │                │   Voiceover  │  │
│              │  (Replicate) │                │ (ElevenLabs) │  │
│              └──────┬───────┘                └──────┬───────┘  │
│                     │                               │          │
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

## Step-by-Step Breakdown

### 1. Intake Form (Tally)

**Fields:**

| Field | Type | Purpose |
|-------|------|---------|
| Business name | text | Context |
| What do you sell/offer? | textarea | Core message |
| Who is your customer? | textarea | Audience targeting |
| What makes you different? | textarea | Hook material |
| Tone preference | select | Friendly / Professional / Bold |
| Language | select | NL / EN / Both |
| Any specific topic for this video? | textarea | Optional focus |
| Reference links (optional) | url | Style reference |

**On submit:** Webhook fires to n8n.

---

### 2. Parse & Validate (n8n)

- Extract form fields
- Look up client in database (match by email or create new)
- Check: has this client exceeded their monthly video quota?
- Check: is there already a video in progress for this client?
- If blocked → notify, halt pipeline
- If clear → proceed

---

### 3. Generate Script (LLM)

**Prompt template:**

```
You are a short-form video scriptwriter for Dutch small businesses.

CLIENT CONTEXT:
- Business: {{business_name}}
- Offer: {{what_they_sell}}
- Audience: {{target_customer}}
- Differentiator: {{what_makes_different}}
- Tone: {{tone_preference}}
- Language: {{language}}
- Topic focus: {{specific_topic}}

TASK:
Write a 30–45 second video script for Instagram Reels / TikTok.

REQUIREMENTS:
- Strong hook in first 2 seconds
- Clear single message
- Call to action at end
- {{language}} language
- {{tone_preference}} tone
- 5–7 scenes maximum

OUTPUT FORMAT:
Return JSON:
{
  "hook": "Opening line (2-3 seconds)",
  "scenes": [
    {"text": "Scene 1 narration", "duration": 5},
    {"text": "Scene 2 narration", "duration": 6},
    ...
  ],
  "cta": "Closing call to action",
  "total_duration": 35
}
```

**Model:** Claude Sonnet (via API) or GPT-4o

**Output:** Structured script JSON

---

### 4. Generate Image Prompts (LLM)

**Input:** Script JSON from step 3

**Prompt template:**

```
You are a visual director for short-form video content.

SCRIPT:
{{script_json}}

BRAND CONTEXT:
- Industry: {{industry}}
- Colours: {{brand_colours}}
- Style: Clean, modern, European, slightly desaturated

TASK:
Generate an image prompt for each scene. Images will be generated by Flux.

REQUIREMENTS:
- Photorealistic or clean illustration style (match brand)
- No text in images
- Consistent visual style across all scenes
- Safe for work
- Appropriate for Dutch business audience

OUTPUT FORMAT:
Return JSON:
{
  "prompts": [
    {"scene": 1, "prompt": "..."},
    {"scene": 2, "prompt": "..."},
    ...
  ]
}
```

**Output:** Array of image prompts

---

### 5. Generate Images (Replicate — Parallel)

**Model:** Flux Schnell (fast) or Flux Dev (quality)

**For each prompt:**
```python
replicate.run(
    "black-forest-labs/flux-schnell",
    input={
        "prompt": scene_prompt,
        "aspect_ratio": "9:16",
        "num_outputs": 1
    }
)
```

**Run in parallel** — all scenes simultaneously.

**Output:** Array of image URLs

**Cost logging:** ~$0.003 per image × 5–7 images = ~$0.02 per video

---

### 6. Generate Voiceover (ElevenLabs)

**Input:** Full script text (concatenated scenes)

**API call:**
```python
# Combine script
full_script = script["hook"] + " " + " ".join([s["text"] for s in script["scenes"]]) + " " + script["cta"]

# Generate
audio = elevenlabs.generate(
    text=full_script,
    voice="Dutch_Male_Calm",  # or per-client preset
    model="eleven_multilingual_v2"
)
```

**Output:** Audio file (MP3/WAV)

**Cost logging:** ~$0.30 per 1000 characters. 30-sec script ≈ 400 chars ≈ $0.12

---

### 7. Assemble Video (FFmpeg)

**Inputs:**
- Images (5–7)
- Audio file
- Music track (from library, optional)
- Brand assets (logo watermark)

**Assembly logic:**

```python
# Pseudocode
def assemble_video(images, audio, script, music=None):
    # Calculate timing per scene from script durations
    # Or: detect audio segments and sync
    
    # For each scene:
    #   - Add image as clip (with Ken Burns zoom/pan)
    #   - Duration from script or audio timing
    
    # Add audio track
    # Add music track (lowered volume)
    # Add logo watermark (bottom corner)
    # Add captions (optional, from script)
    
    # Export: 1080x1920 (9:16)
    
    return output_path
```

**Implementation options:**
- FFmpeg directly (most control)
- MoviePy (Python wrapper, easier)
- Remotion (if moving to JS pipeline)

**Output:** Draft video file (MP4)

---

### 8. Create Draft & Notify

- Save video to storage
- Create Video record in database (status: `draft`)
- Create notification for Jeroen
- Optionally: auto-generate caption draft

**Notification (Slack/Email):**
```
New draft video ready for review

Client: {{client_name}}
Topic: {{specific_topic}}
Duration: {{total_duration}}s

[Review in Engine →]
```

---

## Quality Gates

| Gate | Check | Action on Fail |
|------|-------|----------------|
| Form spam | Rate limit per email (1/day) | Reject, notify |
| Script generation | JSON parse success | Retry once, then flag for manual |
| Image generation | All images returned | Retry failed, proceed with partial |
| Audio generation | File > 5 seconds | Retry, then flag |
| Assembly | Output file exists, > 10 seconds | Flag for manual |

---

## Cost Controls

| Step | Cost | Control |
|------|------|---------|
| LLM (script) | ~$0.01 | Low, no gate needed |
| LLM (prompts) | ~$0.01 | Low, no gate needed |
| Replicate | ~$0.02 | Log per-project |
| ElevenLabs | ~$0.15 | Log per-project, monthly cap per client |
| HeyGen (if used) | ~$1–2 | Manual approval required before generation |

**Total automated cost per video:** ~$0.20–0.30 (no avatar)

At 8 videos/month × 20 clients = 160 videos = ~$40/month in API costs.

---

## n8n Workflow Structure

```
Workflow: "Auto Video Pipeline"

Trigger: Webhook (Tally form)
    │
    ├─► Parse JSON
    │
    ├─► HTTP Request: Check client quota (your API)
    │       └─► If exceeded → Send rejection email → Stop
    │
    ├─► HTTP Request: Generate script (Claude API)
    │
    ├─► HTTP Request: Generate image prompts (Claude API)
    │
    ├─► Split: For each prompt
    │       └─► HTTP Request: Replicate (parallel)
    │
    ├─► Merge: Collect image URLs
    │
    ├─► HTTP Request: ElevenLabs
    │
    ├─► HTTP Request: Your API — assemble video (triggers server-side FFmpeg)
    │
    ├─► HTTP Request: Your API — create draft record
    │
    └─► Slack/Email: Notify Jeroen
```

---

## What This Unlocks

| Before | After |
|--------|-------|
| Jeroen writes script | Script generated from intake |
| Jeroen generates images manually | Images generated automatically |
| Jeroen records/generates VO | VO generated automatically |
| Jeroen assembles in editor | Video assembled automatically |
| Jeroen uploads for review | Draft appears in review queue |

**Jeroen's role becomes:** Review, refine, approve. Creative direction, not production labour.

---

## Limitations / Honest Caveats

1. **Quality variance** — LLM scripts won't always nail the hook. Plan for 20–30% needing manual rewrite.
2. **Image coherence** — Flux doesn't guarantee consistent style across scenes. May need prompt engineering or manual swap.
3. **Audio sync** — Auto-timing is approximate. Some videos will need manual adjustment.
4. **No avatar in auto-flow** — HeyGen is too expensive and slow for full automation. Keep avatar videos manual.

---

## Suggested Implementation Order

| Step | What | Effort |
|------|------|--------|
| 1 | Tally form + n8n webhook | 1 day |
| 2 | Script generation prompt + test | 1 day |
| 3 | Image prompt generation + test | 1 day |
| 4 | Replicate integration | 1 day |
| 5 | ElevenLabs integration | 1 day |
| 6 | FFmpeg assembly endpoint | 2–3 days |
| 7 | Full pipeline in n8n | 1–2 days |
| 8 | Review queue in Engine | 1 day |

**Total: ~10–12 days** to automated draft pipeline.

---

*End of pipeline spec.*
