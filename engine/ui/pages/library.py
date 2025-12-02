"""Library page - video content library."""

import flet as ft
from ui.theme import COLORS, SPACING
from ui.layout import page_header
from ui.components.video_card import video_card
from core.api import api_client


def library_page(page: ft.Page) -> ft.Control:
    """Build the library page."""

    # Fetch videos from API
    videos = api_client.get_videos()

    # Build video cards
    video_cards = []
    for video in videos:
        video_cards.append(
            video_card(
                title=video.get("title", "Untitled"),
                status=video.get("status", "draft"),
                on_click=lambda e, v=video: None,  # TODO: Open video detail
            )
        )

    # Fallback if no videos
    if not video_cards:
        video_cards = [
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.VIDEO_LIBRARY_OUTLINED, size=48, color=COLORS["steel"]),
                        ft.Text("No videos yet", color=COLORS["steel"]),
                        ft.Text("Create your first video to get started", size=12, color=COLORS["steel"]),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=SPACING["sm"],
                ),
                padding=SPACING["xl"],
                alignment=ft.alignment.center,
                expand=True,
            )
        ]

    return ft.Column(
        controls=[
            page_header(
                title="Content Library",
                subtitle="All your videos in one place",
            ),

            # Filters
            ft.Row(
                controls=[
                    ft.Dropdown(
                        label="Status",
                        width=150,
                        options=[
                            ft.dropdown.Option("all", "All"),
                            ft.dropdown.Option("draft", "Draft"),
                            ft.dropdown.Option("review", "Review"),
                            ft.dropdown.Option("approved", "Approved"),
                            ft.dropdown.Option("delivered", "Delivered"),
                        ],
                        value="all",
                    ),
                    ft.Container(expand=True),
                    ft.TextField(
                        hint_text="Search videos...",
                        prefix_icon=ft.Icons.SEARCH,
                        width=300,
                        border_radius=6,
                    ),
                ],
                spacing=SPACING["md"],
            ),

            ft.Container(height=SPACING["lg"]),

            # Video grid
            ft.Row(
                controls=video_cards,
                wrap=True,
                spacing=SPACING["md"],
                run_spacing=SPACING["md"],
            ),
        ],
    )
