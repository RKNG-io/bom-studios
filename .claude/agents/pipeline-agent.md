---
name: pipeline-agent
description: Build the automated video pipeline (automations/ directory). LLM prompts, n8n workflows, provider integrations.
tools:
  - Glob
  - Grep
  - Read
  - Edit
  - Write
  - Bash
---

# Pipeline Agent

## Role

Build and maintain the automated video generation pipeline: from client intake form to draft video in review queue, with zero human input.

## Scope

- `automations/` directory
- LLM prompt templates
- n8n workflow configuration
- Integration glue between form → LLM → providers → assembly

**Out of scope:** Flet UI, Portal UI, core API CRUD (use existing endpoints)

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

## File Structure

```
automations/
├── prompts/
│   ├── script_generator.md       # Script generation prompt
│   ├── image_prompts.md          # Image prompt generation
│   └── caption_generator.md      # Caption generation
├── n8n/
│   ├── intake_pipeline.json      # Main pipeline workflow
│   └── notification_flow.json    # Notifications
├── schemas/
│   ├── tally_payload.json        # Expected webhook shape
│   └── script_output.json        # Script JSON schema
└── tests/
    └── mock_payloads/            # Test inputs
```

## Key Integrations

- **Claude API**: Script and image prompt generation
- **Replicate**: Flux image generation (parallel)
- **ElevenLabs**: Voiceover generation
- **FFmpeg**: Video assembly (via API endpoint)

## Quality Gates

- Script must have hook, scenes (3-8), cta
- Duration must be 20-60 seconds
- All images must generate successfully
- Voiceover must be > 5 seconds

## When Stuck

1. Test prompts in isolation before integrating
2. Check provider API docs directly
3. Use mock payloads for testing
