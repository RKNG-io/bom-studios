"""Image generation service using Replicate (Flux)."""

import asyncio
from typing import Optional

import httpx

from config import get_settings

settings = get_settings()


async def generate_image(
    prompt: str,
    aspect_ratio: str = "9:16",
    num_outputs: int = 1,
) -> list[str]:
    """
    Generate an image using Replicate's Flux model.

    Returns a list of image URLs.
    """
    if not settings.replicate_api_token:
        raise ValueError("REPLICATE_API_TOKEN not configured")

    async with httpx.AsyncClient() as client:
        # Start prediction
        response = await client.post(
            "https://api.replicate.com/v1/predictions",
            headers={
                "Authorization": f"Token {settings.replicate_api_token}",
                "Content-Type": "application/json",
            },
            json={
                "version": "black-forest-labs/flux-schnell",
                "input": {
                    "prompt": prompt,
                    "aspect_ratio": aspect_ratio,
                    "num_outputs": num_outputs,
                    "output_format": "png",
                },
            },
            timeout=30.0,
        )
        response.raise_for_status()
        prediction = response.json()

        # Poll for completion
        prediction_url = prediction["urls"]["get"]
        max_attempts = 60  # 60 seconds max wait
        for _ in range(max_attempts):
            response = await client.get(
                prediction_url,
                headers={"Authorization": f"Token {settings.replicate_api_token}"},
                timeout=10.0,
            )
            response.raise_for_status()
            result = response.json()

            if result["status"] == "succeeded":
                return result["output"]
            elif result["status"] == "failed":
                raise RuntimeError(f"Image generation failed: {result.get('error')}")

            await asyncio.sleep(1)

        raise TimeoutError("Image generation timed out")


async def generate_images_parallel(
    prompts: list[str],
    aspect_ratio: str = "9:16",
) -> list[str]:
    """
    Generate multiple images in parallel.

    Returns a list of image URLs in the same order as prompts.
    """
    tasks = [generate_image(prompt, aspect_ratio) for prompt in prompts]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    urls = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            raise RuntimeError(f"Failed to generate image {i}: {result}")
        # Each result is a list, take the first image
        urls.append(result[0] if result else None)

    return urls
