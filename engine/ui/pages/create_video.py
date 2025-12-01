"""Create video page - wizard for video creation."""

import flet as ft
from ui.theme import COLORS, SPACING
from ui.layout import page_header
from ui.components.card import card
from ui.components.button import primary_button, secondary_button
from ui.components.input import text_area, text_input


def _build_progress(step: int) -> ft.Container:
    """Progress indicator for wizard steps."""
    steps = ["Script", "Visuals", "Audio", "Preview", "Export"]

    step_controls = []
    for i, step_name in enumerate(steps):
        step_controls.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            str(i + 1),
                            size=14,
                            weight=ft.FontWeight.W_500,
                            color=COLORS["paper_white"] if i + 1 <= step else COLORS["steel"],
                        ),
                        width=32,
                        height=32,
                        bgcolor=COLORS["black"] if i + 1 <= step else COLORS["silver"],
                        border_radius=16,
                        alignment=ft.alignment.center,
                    ),
                    ft.Text(
                        step_name,
                        size=14,
                        color=COLORS["black"] if i + 1 <= step else COLORS["steel"],
                    ),
                ],
                spacing=SPACING["xs"],
            )
        )
        if i < len(steps) - 1:
            step_controls.append(
                ft.Container(
                    width=40,
                    height=2,
                    bgcolor=COLORS["black"] if i + 1 < step else COLORS["silver"],
                )
            )

    return ft.Container(
        content=ft.Row(
            controls=step_controls,
            spacing=SPACING["sm"],
        ),
    )


def _step_script(data: dict) -> ft.Container:
    """Step 1: Script input."""
    return card(
        content=ft.Column(
            controls=[
                ft.Text("Write Your Script", size=24, weight=ft.FontWeight.W_500),
                ft.Text(
                    "Enter the video script. Include hook, main content, and call to action.",
                    size=14,
                    color=COLORS["steel"],
                ),
                ft.Container(height=SPACING["md"]),
                text_input(
                    label="Video Title",
                    hint="e.g., Product Launch Video",
                    value=data.get("title", ""),
                ),
                ft.Container(height=SPACING["sm"]),
                text_area(
                    label="Script",
                    hint="Hook: Start with attention-grabbing opening...\n\nMain content: Explain your key message...\n\nCTA: End with a clear call to action...",
                    value=data.get("script", ""),
                    min_lines=10,
                    max_lines=20,
                ),
                ft.Container(height=SPACING["sm"]),
                ft.Row(
                    controls=[
                        ft.Text("~30-45 seconds recommended", size=12, color=COLORS["steel"]),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
        ),
        padding=SPACING["lg"],
    )


def _step_visuals() -> ft.Container:
    """Step 2: Visual generation."""
    return card(
        content=ft.Column(
            controls=[
                ft.Text("Generate Visuals", size=24, weight=ft.FontWeight.W_500),
                ft.Text(
                    "Generate images for each scene using AI.",
                    size=14,
                    color=COLORS["steel"],
                ),
                ft.Container(height=SPACING["md"]),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.IMAGE_OUTLINED, size=48, color=COLORS["steel"]),
                            ft.Text("Click to generate images from script", color=COLORS["steel"]),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=SPACING["sm"],
                    ),
                    padding=SPACING["xl"],
                    bgcolor=COLORS["warm_white"],
                    border=ft.border.all(2, COLORS["silver"]),
                    border_radius=8,
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=SPACING["md"]),
                primary_button(
                    text="Generate Images",
                    icon=ft.Icons.AUTO_AWESOME,
                ),
                ft.Text(
                    "Estimated cost: ~€0.02 (5 images)",
                    size=12,
                    color=COLORS["steel"],
                ),
            ],
        ),
        padding=SPACING["lg"],
    )


def _step_audio() -> ft.Container:
    """Step 3: Audio upload or generation."""
    return card(
        content=ft.Column(
            controls=[
                ft.Text("Add Audio", size=24, weight=ft.FontWeight.W_500),
                ft.Text(
                    "Upload voiceover or generate using AI.",
                    size=14,
                    color=COLORS["steel"],
                ),
                ft.Container(height=SPACING["md"]),
                ft.Row(
                    controls=[
                        secondary_button(
                            text="Upload Audio",
                            icon=ft.Icons.UPLOAD_FILE,
                        ),
                        primary_button(
                            text="Generate with AI",
                            icon=ft.Icons.RECORD_VOICE_OVER,
                        ),
                    ],
                    spacing=SPACING["md"],
                ),
                ft.Container(height=SPACING["md"]),
                ft.Text(
                    "AI generation cost: ~€0.12",
                    size=12,
                    color=COLORS["steel"],
                ),
            ],
        ),
        padding=SPACING["lg"],
    )


def _step_preview() -> ft.Container:
    """Step 4: Preview assembled video."""
    return card(
        content=ft.Column(
            controls=[
                ft.Text("Preview", size=24, weight=ft.FontWeight.W_500),
                ft.Text(
                    "Review your video before exporting.",
                    size=14,
                    color=COLORS["steel"],
                ),
                ft.Container(height=SPACING["md"]),
                ft.Container(
                    content=ft.Icon(ft.Icons.PLAY_CIRCLE_FILLED, size=64, color=COLORS["steel"]),
                    width=360,
                    height=640,
                    bgcolor=COLORS["black"],
                    border_radius=8,
                    alignment=ft.alignment.center,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=SPACING["lg"],
    )


def _step_export() -> ft.Container:
    """Step 5: Export options."""
    return card(
        content=ft.Column(
            controls=[
                ft.Text("Export Video", size=24, weight=ft.FontWeight.W_500),
                ft.Text(
                    "Choose formats and export your video.",
                    size=14,
                    color=COLORS["steel"],
                ),
                ft.Container(height=SPACING["md"]),
                ft.Text("Select formats:", size=14, weight=ft.FontWeight.W_500),
                ft.Checkbox(label="Vertical (9:16) - Reels, TikTok, Shorts", value=True),
                ft.Checkbox(label="Square (1:1) - Feed posts"),
                ft.Checkbox(label="Horizontal (16:9) - YouTube"),
                ft.Container(height=SPACING["md"]),
                primary_button(
                    text="Export Selected",
                    icon=ft.Icons.DOWNLOAD,
                ),
            ],
        ),
        padding=SPACING["lg"],
    )


def create_video_page(page: ft.Page) -> ft.Control:
    """Build the create video page."""
    # Get or initialize wizard state
    step = page.session.get("wizard_step") or 1
    data = page.session.get("wizard_data") or {"title": "", "script": ""}

    def next_step(e):
        current = page.session.get("wizard_step") or 1
        if current < 5:
            page.session.set("wizard_step", current + 1)
            page.go("/create")

    def prev_step(e):
        current = page.session.get("wizard_step") or 1
        if current > 1:
            page.session.set("wizard_step", current - 1)
            page.go("/create")

    # Build step content
    if step == 1:
        step_content = _step_script(data)
    elif step == 2:
        step_content = _step_visuals()
    elif step == 3:
        step_content = _step_audio()
    elif step == 4:
        step_content = _step_preview()
    else:
        step_content = _step_export()

    return ft.Column(
        controls=[
            page_header(
                title="Create Video",
                subtitle="Step-by-step video creation wizard",
            ),
            _build_progress(step),
            ft.Container(height=SPACING["lg"]),
            step_content,
            ft.Container(height=SPACING["lg"]),
            # Navigation
            ft.Row(
                controls=[
                    secondary_button(
                        text="Back",
                        on_click=prev_step,
                    ) if step > 1 else ft.Container(),
                    ft.Container(expand=True),
                    primary_button(
                        text="Next" if step < 5 else "Finish",
                        on_click=next_step,
                    ),
                ],
            ),
        ],
    )
