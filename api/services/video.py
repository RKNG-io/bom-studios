"""Video assembly service using FFmpeg."""

import asyncio
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

import httpx


async def download_file(url: str, dest: Path) -> None:
    """Download a file from URL to local path."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url, follow_redirects=True, timeout=60.0)
        response.raise_for_status()
        dest.write_bytes(response.content)


async def assemble_video(
    image_urls: list[str],
    audio_url: str,
    output_format: str = "vertical",
    music_url: Optional[str] = None,
    duration_per_image: float = 5.0,
) -> Path:
    """
    Assemble a video from images and audio using FFmpeg.

    Args:
        image_urls: List of image URLs for each scene
        audio_url: URL to the voiceover audio file
        output_format: 'vertical' (9:16), 'square' (1:1), or 'horizontal' (16:9)
        music_url: Optional background music URL
        duration_per_image: Seconds per image (used if no audio timing)

    Returns:
        Path to the output video file
    """
    # Create temp directory for assets
    temp_dir = Path(tempfile.mkdtemp(prefix="bom_video_"))

    try:
        # Download all assets in parallel
        download_tasks = []

        # Download images
        image_paths = []
        for i, url in enumerate(image_urls):
            path = temp_dir / f"img_{i:03d}.png"
            image_paths.append(path)
            download_tasks.append(download_file(url, path))

        # Download audio
        audio_path = temp_dir / "audio.mp3"
        download_tasks.append(download_file(audio_url, audio_path))

        # Download music if provided
        music_path = None
        if music_url:
            music_path = temp_dir / "music.mp3"
            download_tasks.append(download_file(music_url, music_path))

        await asyncio.gather(*download_tasks)

        # Determine output dimensions based on format
        dimensions = {
            "vertical": (1080, 1920),
            "square": (1080, 1080),
            "horizontal": (1920, 1080),
        }
        width, height = dimensions.get(output_format, (1080, 1920))

        # Get audio duration
        probe_cmd = [
            "ffprobe",
            "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "csv=p=0",
            str(audio_path),
        ]
        result = subprocess.run(probe_cmd, capture_output=True, text=True)
        audio_duration = float(result.stdout.strip()) if result.stdout.strip() else 30.0

        # Calculate duration per image based on audio length
        if image_paths:
            duration_per_image = audio_duration / len(image_paths)

        # Create concat file for images
        concat_file = temp_dir / "concat.txt"
        with open(concat_file, "w") as f:
            for path in image_paths:
                f.write(f"file '{path}'\n")
                f.write(f"duration {duration_per_image}\n")
            # Add last image again (FFmpeg concat quirk)
            if image_paths:
                f.write(f"file '{image_paths[-1]}'\n")

        output_path = temp_dir / "output.mp4"

        # Build FFmpeg command
        cmd = [
            "ffmpeg",
            "-y",  # Overwrite output
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-i", str(audio_path),
        ]

        # Add music if present
        filter_complex = []
        if music_path:
            cmd.extend(["-i", str(music_path)])
            # Mix audio tracks - voiceover at full volume, music at 20%
            filter_complex.append("[1:a]volume=1.0[vo]")
            filter_complex.append("[2:a]volume=0.2[music]")
            filter_complex.append("[vo][music]amix=inputs=2:duration=first[aout]")
            audio_map = "[aout]"
        else:
            audio_map = "1:a"

        # Video filters: scale and pad to target dimensions with Ken Burns effect
        video_filter = (
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black,"
            f"zoompan=z='min(zoom+0.001,1.1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(duration_per_image * 25)}:s={width}x{height}:fps=25"
        )

        if filter_complex:
            filter_complex.insert(0, f"[0:v]{video_filter}[vout]")
            cmd.extend(["-filter_complex", ";".join(filter_complex)])
            cmd.extend(["-map", "[vout]", "-map", audio_map])
        else:
            cmd.extend(["-vf", video_filter])
            cmd.extend(["-map", "0:v", "-map", audio_map])

        # Output settings
        cmd.extend([
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "128k",
            "-shortest",
            "-movflags", "+faststart",
            str(output_path),
        ])

        # Run FFmpeg
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f"FFmpeg failed: {stderr.decode()}")

        return output_path

    except Exception:
        # Clean up on error (but keep temp_dir for debugging)
        raise


async def assemble_video_simple(
    image_urls: list[str],
    audio_url: str,
    output_format: str = "vertical",
) -> Path:
    """
    Simpler video assembly without Ken Burns effect.

    Faster processing, less fancy.
    """
    temp_dir = Path(tempfile.mkdtemp(prefix="bom_video_"))

    # Download assets
    image_paths = []
    for i, url in enumerate(image_urls):
        path = temp_dir / f"img_{i:03d}.png"
        await download_file(url, path)
        image_paths.append(path)

    audio_path = temp_dir / "audio.mp3"
    await download_file(audio_url, audio_path)

    # Get audio duration
    probe_cmd = [
        "ffprobe", "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        str(audio_path),
    ]
    result = subprocess.run(probe_cmd, capture_output=True, text=True)
    audio_duration = float(result.stdout.strip()) if result.stdout.strip() else 30.0
    duration_per_image = audio_duration / len(image_paths) if image_paths else 5.0

    # Dimensions
    dimensions = {"vertical": (1080, 1920), "square": (1080, 1080), "horizontal": (1920, 1080)}
    width, height = dimensions.get(output_format, (1080, 1920))

    # Create concat file
    concat_file = temp_dir / "concat.txt"
    with open(concat_file, "w") as f:
        for path in image_paths:
            f.write(f"file '{path}'\n")
            f.write(f"duration {duration_per_image}\n")
        if image_paths:
            f.write(f"file '{image_paths[-1]}'\n")

    output_path = temp_dir / "output.mp4"

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-i", str(audio_path),
        "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest", "-movflags", "+faststart",
        str(output_path),
    ]

    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {stderr.decode()}")

    return output_path
