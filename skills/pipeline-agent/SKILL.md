# SKILL.md — Pipeline Agent

## Role

Build and maintain the automated video generation pipeline: from client intake form to draft video in review queue, with zero human input.

---

## Scope

- `automations/` directory
- LLM prompt templates
- n8n workflow configuration
- Integration glue between form → LLM → providers → assembly

**Out of scope:** Flet UI, Portal UI, core API CRUD (use existing endpoints)

---

## Pipeline Overview

```
Intake Form (Tally)
    ↓ webhook
Parse & Validate
    ↓
LLM: Generate Script (Claude)
    ↓
LLM: Generate Image Prompts (Claude)
    ↓
Generate Images (Replicate Flux) [parallel]
    ↓
Generate Voiceover (ElevenLabs)
    ↓
Assemble Video (FFmpeg)
    ↓
Create Draft Record
    ↓
Notify Jeroen (Slack)
```

**Total automated cost per video:** ~€0.20–0.30

---

## File Structure

```
automations/
├── prompts/
│   ├── script_generator.md       # Script generation prompt
│   ├── image_prompts.md          # Image prompt generation
│   └── caption_generator.md      # Caption generation (Phase 3)
├── n8n/
│   ├── intake_pipeline.json      # Main pipeline workflow export
│   ├── notification_flow.json    # Slack/email notifications
│   └── README.md                 # n8n setup instructions
├── schemas/
│   ├── tally_payload.json        # Expected Tally webhook shape
│   ├── script_output.json        # Script generation output schema
│   └── pipeline_events.json      # Event definitions
└── tests/
    ├── test_prompts.py           # Prompt output validation
    └── mock_payloads/            # Test webhook payloads
```

---

## Task Queue

### Phase 2.5 (Pipeline MVP)

- [ ] `prompts/script_generator.md` — Full prompt with examples
- [ ] `prompts/image_prompts.md` — Image prompt generation
- [ ] `schemas/tally_payload.json` — Document expected fields
- [ ] `schemas/script_output.json` — JSON schema for validation
- [ ] Test script generation with 5 sample inputs
- [ ] Test image prompt generation
- [ ] `n8n/intake_pipeline.json` — Full workflow
- [ ] End-to-end test: form → draft video

### Phase 3 (Enhancements)

- [ ] `prompts/caption_generator.md` — Social captions
- [ ] Multi-language support (NL/EN branching)
- [ ] Retry logic for failed generations
- [ ] Cost tracking per pipeline run

---

## Prompt Templates

### Script Generator

```markdown
# prompts/script_generator.md

## System

You are a short-form video scriptwriter for Dutch small businesses. You write punchy, clear scripts for Instagram Reels, TikTok, and YouTube Shorts.

## Context

CLIENT:
- Business: {{business_name}}
- Offer: {{what_they_sell}}
- Audience: {{target_customer}}
- Differentiator: {{what_makes_different}}
- Tone: {{tone}} (friendly / professional / bold)
- Language: {{language}} (NL / EN)
- Topic focus: {{topic}} (optional)

## Task

Write a 30–45 second video script.

## Requirements

1. Hook in first 2 seconds — pattern interrupt, question, or bold claim
2. Single clear message — one idea, not three
3. 5–7 scenes maximum
4. Call to action at end
5. Match the requested tone
6. Use {{language}} language throughout

## Output Format

Return ONLY valid JSON, no markdown:

{
  "hook": "Opening line (2-3 seconds)",
  "scenes": [
    {"text": "Scene 1 narration", "visual_hint": "What to show", "duration": 5},
    {"text": "Scene 2 narration", "visual_hint": "What to show", "duration": 6}
  ],
  "cta": "Closing call to action",
  "total_duration": 35
}

## Examples

INPUT:
- Business: Amsterdam Coffee Roasters
- Offer: Specialty coffee beans, home delivery
- Audience: Coffee enthusiasts, home brewers
- Differentiator: Single-origin, roasted weekly, delivered next day
- Tone: friendly
- Language: EN

OUTPUT:
{
  "hook": "Your coffee is stale. Here's why.",
  "scenes": [
    {"text": "Most supermarket coffee was roasted months ago.", "visual_hint": "Sad coffee bag on shelf", "duration": 4},
    {"text": "By the time you brew it, the flavour is gone.", "visual_hint": "Pouring bland coffee", "duration": 4},
    {"text": "We roast every week. Single origin beans from Colombia, Ethiopia, Guatemala.", "visual_hint": "Fresh roasting process", "duration": 6},
    {"text": "Order today, it's at your door tomorrow.", "visual_hint": "Package arriving", "duration": 4},
    {"text": "Taste the difference fresh makes.", "visual_hint": "Someone enjoying coffee", "duration": 4}
  ],
  "cta": "Link in bio. First bag, 20% off.",
  "total_duration": 26
}
```

### Image Prompts Generator

```markdown
# prompts/image_prompts.md

## System

You are a visual director for short-form video. You write image generation prompts for Flux that produce consistent, professional visuals.

## Context

SCRIPT:
{{script_json}}

BRAND:
- Industry: {{industry}}
- Colours: {{brand_colours}} (if available)
- Style preference: Clean, modern, European aesthetic. Slightly desaturated. Natural lighting.

## Task

Generate one image prompt per scene.

## Requirements

1. Photorealistic or clean illustration (match industry)
2. NO text in images — Flux can't render text well
3. Consistent visual style across ALL scenes
4. Safe for work, professional
5. Suitable for vertical video (9:16 framing)
6. Include lighting and mood guidance

## Output Format

Return ONLY valid JSON:

{
  "style_guide": "Brief description of overall visual style",
  "prompts": [
    {"scene": 1, "prompt": "Full image generation prompt..."},
    {"scene": 2, "prompt": "Full image generation prompt..."}
  ]
}

## Prompt Structure

Each prompt should follow this pattern:
"[Subject/action], [setting/background], [lighting], [mood], [style modifiers], vertical composition, 9:16 aspect ratio"

## Example

SCRIPT: Coffee roasters video (from previous example)

OUTPUT:
{
  "style_guide": "Warm, inviting coffee shop aesthetic. Natural morning light. Slightly desaturated colours with warm highlights.",
  "prompts": [
    {"scene": 1, "prompt": "Dusty old coffee bag sitting on supermarket shelf under harsh fluorescent lighting, dull colours, commercial photography style, vertical composition, 9:16 aspect ratio"},
    {"scene": 2, "prompt": "Close-up of bland watery coffee being poured into plain white mug, grey overcast window light, muted tones, product photography, vertical composition, 9:16 aspect ratio"},
    {"scene": 3, "prompt": "Coffee beans tumbling in professional roasting drum, warm amber glow, smoke wisps, artisan workshop setting, cinematic lighting, vertical composition, 9:16 aspect ratio"},
    {"scene": 4, "prompt": "Cardboard delivery package on doorstep of modern Amsterdam canal house, morning golden hour light, welcoming atmosphere, lifestyle photography, vertical composition, 9:16 aspect ratio"},
    {"scene": 5, "prompt": "Young professional smelling fresh coffee from ceramic cup, eyes closed in enjoyment, soft window light, cozy kitchen background, warm tones, portrait style, vertical composition, 9:16 aspect ratio"}
  ]
}
```

---

## Tally Form Fields

```json
// schemas/tally_payload.json
{
  "fields": {
    "business_name": {
      "type": "text",
      "required": true,
      "tally_id": "question_xyz"
    },
    "email": {
      "type": "email",
      "required": true,
      "tally_id": "question_abc"
    },
    "what_they_sell": {
      "type": "textarea",
      "required": true,
      "tally_id": "question_def"
    },
    "target_customer": {
      "type": "textarea",
      "required": true,
      "tally_id": "question_ghi"
    },
    "what_makes_different": {
      "type": "textarea",
      "required": true,
      "tally_id": "question_jkl"
    },
    "tone": {
      "type": "select",
      "options": ["friendly", "professional", "bold"],
      "default": "friendly",
      "tally_id": "question_mno"
    },
    "language": {
      "type": "select",
      "options": ["NL", "EN"],
      "default": "EN",
      "tally_id": "question_pqr"
    },
    "topic": {
      "type": "textarea",
      "required": false,
      "tally_id": "question_stu"
    }
  }
}
```

---

## n8n Workflow Structure

```
Workflow: "BOM Video Pipeline"

[Webhook Trigger]
    │ POST /webhook/tally-intake
    │
    ▼
[Parse Tally Payload]
    │ Extract fields, normalize
    │
    ▼
[HTTP Request: Check Client]
    │ GET /api/clients?email={{email}}
    │ If not found → create client
    │
    ▼
[HTTP Request: Check Quota]
    │ GET /api/clients/{{id}}/quota
    │ If exceeded → branch to rejection flow
    │
    ▼
[HTTP Request: Generate Script]
    │ POST to Claude API
    │ Body: script_generator prompt with variables
    │
    ▼
[Parse Script JSON]
    │ Validate structure
    │ Extract scenes
    │
    ▼
[HTTP Request: Generate Image Prompts]
    │ POST to Claude API
    │ Body: image_prompts prompt with script
    │
    ▼
[Split: For Each Prompt]
    │
    ├──► [HTTP Request: Replicate]
    ├──► [HTTP Request: Replicate]
    ├──► [HTTP Request: Replicate]
    ├──► [HTTP Request: Replicate]
    └──► [HTTP Request: Replicate]
    │
    ▼
[Merge: Collect Image URLs]
    │
    ▼
[HTTP Request: ElevenLabs]
    │ Generate voiceover from full script text
    │
    ▼
[HTTP Request: Trigger Assembly]
    │ POST /api/assembly/generate
    │ Body: { video_id, script, images, audio_url }
    │
    ▼
[Wait for Assembly]
    │ Poll /api/assembly/status/{{job_id}}
    │ Or: use callback webhook
    │
    ▼
[HTTP Request: Create Video Record]
    │ POST /api/videos
    │ status: "draft"
    │
    ▼
[Slack Notification]
    │ "New draft video ready for review"
    │
    ▼
[End]
```

---

## API Calls in Pipeline

### Claude API (Script Generation)

```javascript
// n8n HTTP Request node
{
  "method": "POST",
  "url": "https://api.anthropic.com/v1/messages",
  "headers": {
    "x-api-key": "{{$credentials.anthropicApi}}",
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
  },
  "body": {
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1000,
    "messages": [
      {
        "role": "user",
        "content": "{{$node['Build Prompt'].json.prompt}}"
      }
    ]
  }
}
```

### Replicate API (Image Generation)

```javascript
// n8n HTTP Request node
{
  "method": "POST",
  "url": "https://api.replicate.com/v1/predictions",
  "headers": {
    "Authorization": "Token {{$credentials.replicateApi}}",
    "content-type": "application/json"
  },
  "body": {
    "version": "black-forest-labs/flux-schnell",
    "input": {
      "prompt": "{{$json.prompt}}",
      "aspect_ratio": "9:16",
      "num_outputs": 1
    }
  }
}
```

### ElevenLabs API (Voiceover)

```javascript
// n8n HTTP Request node
{
  "method": "POST",
  "url": "https://api.elevenlabs.io/v1/text-to-speech/{{voiceId}}",
  "headers": {
    "xi-api-key": "{{$credentials.elevenlabsApi}}",
    "content-type": "application/json"
  },
  "body": {
    "text": "{{$node['Build Script Text'].json.full_text}}",
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.75
    }
  },
  "responseType": "file"
}
```

---

## Quality Gates

```javascript
// Validation logic in n8n

// After script generation
const script = JSON.parse($json.content[0].text);

if (!script.hook || !script.scenes || !script.cta) {
  throw new Error("Invalid script structure");
}

if (script.scenes.length < 3 || script.scenes.length > 8) {
  throw new Error("Scene count out of range");
}

if (script.total_duration < 20 || script.total_duration > 60) {
  throw new Error("Duration out of range");
}

return { json: script };
```

---

## Cost Tracking

Log costs at each step:

```javascript
// After each API call
const costs = {
  script_generation: 0.01,      // ~1000 tokens
  image_prompts: 0.01,          // ~500 tokens
  replicate_image: 0.003,       // per image
  elevenlabs_voice: 0.00015,    // per character
};

// Calculate total
const totalCost = 
  costs.script_generation +
  costs.image_prompts +
  (costs.replicate_image * numImages) +
  (costs.elevenlabs_voice * scriptCharacters);

// Log to API
await fetch('/api/costs/log', {
  method: 'POST',
  body: JSON.stringify({
    pipeline_run_id: runId,
    project_id: projectId,
    breakdown: costs,
    total_cents: Math.ceil(totalCost * 100),
  }),
});
```

---

## Error Handling

| Step | Error | Action |
|------|-------|--------|
| Script generation | Invalid JSON | Retry once with "Return ONLY JSON" appended |
| Script generation | Off-topic | Flag for manual review |
| Image generation | Timeout | Retry once |
| Image generation | NSFW filter | Use fallback prompt |
| Voiceover | Timeout | Retry once |
| Assembly | FFmpeg error | Flag for manual review |

```javascript
// Retry pattern in n8n
{
  "retry": {
    "enabled": true,
    "maxRetries": 1,
    "waitBetweenRetries": 2000
  }
}
```

---

## Testing

### Test Payloads

```json
// tests/mock_payloads/coffee_shop.json
{
  "business_name": "Amsterdam Coffee Roasters",
  "email": "test@example.com",
  "what_they_sell": "Specialty coffee beans, roasted weekly, delivered to your door",
  "target_customer": "Coffee enthusiasts who brew at home",
  "what_makes_different": "Single-origin beans, roasted every week, next-day delivery",
  "tone": "friendly",
  "language": "EN",
  "topic": "Why fresh roasting matters"
}
```

### Prompt Testing

```python
# tests/test_prompts.py
import json
from anthropic import Anthropic

def test_script_generation():
    client = Anthropic()
    
    with open("prompts/script_generator.md") as f:
        prompt_template = f.read()
    
    with open("tests/mock_payloads/coffee_shop.json") as f:
        payload = json.load(f)
    
    prompt = prompt_template.format(**payload)
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    
    # Validate output
    script = json.loads(response.content[0].text)
    
    assert "hook" in script
    assert "scenes" in script
    assert len(script["scenes"]) >= 3
    assert script["total_duration"] >= 20
```

---

## Handoff Points

- **From Tally:** Webhook triggers pipeline
- **To API Agent:** Pipeline calls API endpoints for client lookup, video creation
- **To Engine Agent:** Draft appears in review queue
- **From API Agent:** Assembly endpoint does the FFmpeg work

---

## When Stuck

1. Check `/docs/bom-studios-auto-pipeline.md` for full pipeline spec
2. Check n8n docs: https://docs.n8n.io/
3. Test prompts in isolation before integrating
4. If provider API changes, check their docs directly
