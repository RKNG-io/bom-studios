"""Library page - video content library."""

import flet as ft
from ui.theme import COLORS, SPACING
from ui.layout import page_header
from ui.components.video_card import video_card


def library_page(page: ft.Page) -> ft.Control:
    """Build the library page."""

    # Sample videos for display
    videos = [
        {"title": "Coffee Shop Intro", "status": "approved"},
        {"title": "Product Feature #1", "status": "delivered"},
        {"title": "Behind the Scenes", "status": "review"},
        {"title": "Customer Testimonial", "status": "generating"},
        {"title": "Weekly Tips #12", "status": "draft"},
        {"title": "Holiday Special", "status": "approved"},
        {"title": "New Menu Items", "status": "delivered"},
        {"title": "Team Introduction", "status": "scripting"},
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
                            ft.dropdown.Option("approved", "Approved"),
                            ft.dropdown.Option("delivered", "Delivered"),
                        ],
                        value="all",
                    ),
                    ft.Dropdown(
                        label="Client",
                        width=200,
                        options=[
                            ft.dropdown.Option("all", "All Clients"),
                            ft.dropdown.Option("coffee", "Amsterdam Coffee"),
                            ft.dropdown.Option("tech", "Tech Gadgets NL"),
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
                controls=[
                    video_card(
                        title=video["title"],
                        status=video["status"],
                        on_click=lambda e: None,  # TODO: Open video detail
                    )
                    for video in videos
                ],
                wrap=True,
                spacing=SPACING["md"],
                run_spacing=SPACING["md"],
            ),
        ],
    )
