"""Voice generation service using ElevenLabs."""

import httpx

from config import get_settings

settings = get_settings()

# Default voice IDs - these would be configured per client
DEFAULT_VOICES = {
    "dutch_male": "pNInz6obpgDQGcFmaJgB",  # Adam
    "dutch_female": "21m00Tcm4TlvDq8ikWAM",  # Rachel
    "english_male": "pNInz6obpgDQGcFmaJgB",
    "english_female": "21m00Tcm4TlvDq8ikWAM",
}


async def generate_voiceover(
    text: str,
    voice_id: str | None = None,
    language: str = "EN",
) -> bytes:
    """
    Generate voiceover audio using ElevenLabs.

    Returns the audio file as bytes (MP3 format).
    """
    if not settings.elevenlabs_api_key:
        raise ValueError("ELEVENLABS_API_KEY not configured")

    # Select voice based on language if not specified
    if not voice_id:
        if language.upper() in ("NL", "DUTCH"):
            voice_id = DEFAULT_VOICES["dutch_male"]
        else:
            voice_id = DEFAULT_VOICES["english_male"]

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={
                "xi-api-key": settings.elevenlabs_api_key,
                "Content-Type": "application/json",
            },
            json={
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75,
                },
            },
            timeout=60.0,
        )
        response.raise_for_status()

        return response.content


def script_to_voiceover_text(script: dict) -> str:
    """Convert a script dict to full voiceover text."""
    parts = [script.get("hook", "")]

    for scene in script.get("scenes", []):
        parts.append(scene.get("text", ""))

    parts.append(script.get("cta", ""))

    return " ".join(part for part in parts if part)
