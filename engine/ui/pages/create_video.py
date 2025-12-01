"""Create video page - wizard for video creation."""

import flet as ft
from ui.theme import COLORS, SPACING
from ui.layout import page_header
from ui.components.card import card
from ui.components.button import primary_button, secondary_button
from ui.components.input import text_area, text_input


class CreateVideoWizard(ft.UserControl):
    """Multi-step video creation wizard."""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.wizard_page = page
        self.step = 1
        self.data = {
            "title": "",
            "script": "",
            "images": [],
            "audio_url": None,
        }

    def build(self):
        return ft.Column(
            controls=[
                self._build_progress(),
                ft.Container(height=SPACING["lg"]),
                self._build_step_content(),
                ft.Container(height=SPACING["lg"]),
                self._build_navigation(),
            ],
        )

    def _build_progress(self) -> ft.Container:
        """Progress indicator for wizard steps."""
        steps = ["Script", "Visuals", "Audio", "Preview", "Export"]

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    str(i + 1),
                                    size=14,
                                    weight=ft.FontWeight.W_500,
                                    color=COLORS["paper_white"] if i + 1 <= self.step else COLORS["steel"],
                                ),
                                width=32,
                                height=32,
                                bgcolor=COLORS["black"] if i + 1 <= self.step else COLORS["silver"],
                                border_radius=16,
                                alignment=ft.alignment.center,
                            ),
                            ft.Text(
                                step_name,
                                size=14,
                                color=COLORS["black"] if i + 1 <= self.step else COLORS["steel"],
                            ),
                            ft.Container(
                                width=40,
                                height=2,
                                bgcolor=COLORS["black"] if i + 1 < self.step else COLORS["silver"],
                            ) if i < len(steps) - 1 else ft.Container(),
                        ],
                        spacing=SPACING["xs"],
                    )
                    for i, step_name in enumerate(steps)
                ],
                spacing=SPACING["sm"],
            ),
        )

    def _build_step_content(self) -> ft.Container:
        """Content for current step."""
        if self.step == 1:
            return self._step_script()
        elif self.step == 2:
            return self._step_visuals()
        elif self.step == 3:
            return self._step_audio()
        elif self.step == 4:
            return self._step_preview()
        else:
            return self._step_export()

    def _step_script(self) -> ft.Container:
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
                        value=self.data["title"],
                        on_change=lambda e: self._update_data("title", e.control.value),
                    ),
                    ft.Container(height=SPACING["sm"]),
                    text_area(
                        label="Script",
                        hint="Hook: Start with attention-grabbing opening...\n\nMain content: Explain your key message...\n\nCTA: End with a clear call to action...",
                        value=self.data["script"],
                        on_change=lambda e: self._update_data("script", e.control.value),
                        min_lines=10,
                        max_lines=20,
                    ),
                    ft.Container(height=SPACING["sm"]),
                    ft.Row(
                        controls=[
                            ft.Text(f"{len(self.data['script'])} characters", size=12, color=COLORS["steel"]),
                            ft.Text("~30-45 seconds recommended", size=12, color=COLORS["steel"]),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
            ),
            padding=SPACING["lg"],
        )

    def _step_visuals(self) -> ft.Container:
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
                                ft.Icon(ft.icons.IMAGE_OUTLINED, size=48, color=COLORS["steel"]),
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
                        icon=ft.icons.AUTO_AWESOME,
                        on_click=lambda e: self._generate_images(),
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

    def _step_audio(self) -> ft.Container:
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
                                icon=ft.icons.UPLOAD_FILE,
                            ),
                            primary_button(
                                text="Generate with AI",
                                icon=ft.icons.RECORD_VOICE_OVER,
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

    def _step_preview(self) -> ft.Container:
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
                        content=ft.Icon(ft.icons.PLAY_CIRCLE_FILLED, size=64, color=COLORS["steel"]),
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

    def _step_export(self) -> ft.Container:
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
                        icon=ft.icons.DOWNLOAD,
                    ),
                ],
            ),
            padding=SPACING["lg"],
        )

    def _build_navigation(self) -> ft.Row:
        """Navigation buttons for wizard."""
        return ft.Row(
            controls=[
                secondary_button(
                    text="Back",
                    on_click=lambda e: self._prev_step(),
                ) if self.step > 1 else ft.Container(),
                ft.Container(expand=True),
                primary_button(
                    text="Next" if self.step < 5 else "Finish",
                    on_click=lambda e: self._next_step(),
                ),
            ],
        )

    def _update_data(self, key: str, value):
        """Update wizard data."""
        self.data[key] = value

    def _next_step(self):
        """Go to next step."""
        if self.step < 5:
            self.step += 1
            self.update()

    def _prev_step(self):
        """Go to previous step."""
        if self.step > 1:
            self.step -= 1
            self.update()

    def _generate_images(self):
        """Trigger image generation."""
        # TODO: Connect to Replicate API
        pass


def create_video_page(page: ft.Page) -> ft.Control:
    """Build the create video page."""
    return ft.Column(
        controls=[
            page_header(
                title="Create Video",
                subtitle="Step-by-step video creation wizard",
            ),
            CreateVideoWizard(page),
        ],
    )
