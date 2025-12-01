"""Webhook handlers for external integrations."""

from typing import Any, Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from database import get_session_context
from models.db import Client, Project, Video

router = APIRouter()


# ---------- Tally Form Webhook ----------

class TallyField(BaseModel):
    key: str
    label: str
    value: Any


class TallySubmission(BaseModel):
    eventId: str
    eventType: str
    createdAt: str
    data: dict


class TallyWebhookResponse(BaseModel):
    status: str
    message: str
    video_id: Optional[str] = None


@router.post("/tally", response_model=TallyWebhookResponse)
async def handle_tally_webhook(
    payload: TallySubmission,
    background_tasks: BackgroundTasks,
):
    """
    Handle Tally form submission webhook.

    Expected form fields:
    - business_name
    - email
    - what_they_sell
    - target_customer
    - what_makes_different
    - tone (friendly/professional/bold)
    - language (NL/EN)
    - topic (optional)
    """
    if payload.eventType != "FORM_RESPONSE":
        return TallyWebhookResponse(
            status="ignored",
            message=f"Ignoring event type: {payload.eventType}",
        )

    # Parse form fields from Tally's nested structure
    fields = payload.data.get("fields", [])
    context = {}
    email = None

    for field in fields:
        key = field.get("key", "").lower().replace(" ", "_")
        value = field.get("value")

        if "email" in key:
            email = value
        elif "business" in key and "name" in key:
            context["business_name"] = value
        elif "sell" in key or "offer" in key:
            context["what_they_sell"] = value
        elif "customer" in key or "audience" in key:
            context["target_customer"] = value
        elif "different" in key or "unique" in key:
            context["what_makes_different"] = value
        elif "tone" in key:
            context["tone"] = value or "friendly"
        elif "language" in key or "lang" in key:
            context["language"] = value or "EN"
        elif "topic" in key:
            context["topic"] = value

    if not email:
        raise HTTPException(status_code=400, detail="Email field required")

    # Queue the video generation pipeline
    background_tasks.add_task(
        run_video_pipeline,
        email=email,
        context=context,
    )

    return TallyWebhookResponse(
        status="accepted",
        message="Video generation queued",
    )


async def run_video_pipeline(email: str, context: dict):
    """
    Background task: Full video generation pipeline.

    1. Get or create client
    2. Create project
    3. Generate script (LLM)
    4. Generate image prompts (LLM)
    5. Generate images (Replicate)
    6. Generate voiceover (ElevenLabs)
    7. Assemble video (FFmpeg)
    8. Create video record
    9. Notify (TODO)
    """
    from services.llm import generate_script, generate_image_prompts
    from services.images import generate_images_parallel
    from services.voice import generate_voiceover, script_to_voiceover_text
    from services.video import assemble_video_simple

    async with get_session_context() as session:
        # 1. Get or create client
        stmt = select(Client).where(Client.email == email)
        result = await session.execute(stmt)
        client = result.scalar_one_or_none()

        if not client:
            client = Client(
                name=context.get("business_name", "Unknown"),
                email=email,
                package="kickstart",
            )
            session.add(client)
            await session.flush()

        # 2. Create project
        project = Project(
            client_id=client.id,
            name=f"Auto: {context.get('topic', 'Video')}",
            status="in_progress",
        )
        session.add(project)
        await session.flush()

        # 3. Create video record (status: scripting)
        video = Video(
            project_id=project.id,
            title=context.get("topic", "Generated Video"),
            status="scripting",
        )
        session.add(video)
        await session.flush()

        try:
            # 4. Generate script
            script = await generate_script(
                business_name=context.get("business_name", ""),
                what_they_sell=context.get("what_they_sell", ""),
                target_customer=context.get("target_customer", ""),
                what_makes_different=context.get("what_makes_different", ""),
                tone=context.get("tone", "friendly"),
                language=context.get("language", "EN"),
                topic=context.get("topic"),
            )
            video.script = script
            video.status = "generating"
            await session.flush()

            # 5. Generate image prompts
            prompts_data = await generate_image_prompts(
                script=script,
                industry=context.get("what_they_sell", "business"),
            )
            prompts = [p["prompt"] for p in prompts_data]

            # 6. Generate images
            image_urls = await generate_images_parallel(prompts)

            # 7. Generate voiceover
            vo_text = script_to_voiceover_text(script)
            audio_bytes = await generate_voiceover(
                text=vo_text,
                language=context.get("language", "EN"),
            )

            # Save audio to temp file and get URL
            # (In production, upload to cloud storage)
            import tempfile
            from pathlib import Path

            audio_path = Path(tempfile.mktemp(suffix=".mp3"))
            audio_path.write_bytes(audio_bytes)
            audio_url = f"file://{audio_path}"  # Local file URL

            # 8. Assemble video
            video.status = "rendering"
            await session.flush()

            output_path = await assemble_video_simple(
                image_urls=image_urls,
                audio_url=audio_url,
                output_format="vertical",
            )

            # 9. Update video record
            video.status = "draft"
            video.formats = {"vertical": str(output_path)}
            # TODO: Calculate actual cost
            video.cost_cents = 30  # ~$0.30 estimate

            # Update project status
            project.status = "review"

        except Exception as e:
            # Mark as failed
            video.status = "scripting"  # Reset to allow retry
            video.approval_note = f"Generation failed: {str(e)}"
            project.status = "draft"
            raise

        # TODO: Send notification to Jeroen


# ---------- Stripe Webhook ----------

@router.post("/stripe")
async def handle_stripe_webhook(
    payload: dict,
):
    """
    Handle Stripe payment webhooks.

    TODO: Implement payment status updates.
    """
    event_type = payload.get("type", "unknown")

    # Log for now
    print(f"Stripe webhook received: {event_type}")

    return {"status": "received", "event_type": event_type}


# ---------- n8n Webhook ----------

class N8nEvent(BaseModel):
    event: str
    data: dict


@router.post("/n8n")
async def handle_n8n_webhook(
    payload: N8nEvent,
):
    """
    Generic webhook for n8n workflow callbacks.

    Used for:
    - Pipeline step completions
    - External triggers
    - Status updates
    """
    print(f"n8n webhook received: {payload.event}")

    return {"status": "received", "event": payload.event}
