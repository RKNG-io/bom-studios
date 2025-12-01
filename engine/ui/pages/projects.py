"""Projects page - list and manage projects."""

import flet as ft
from ui.theme import COLORS, SPACING
from ui.layout import page_header
from ui.components.card import card
from ui.components.button import primary_button, secondary_button
from ui.components.status_badge import status_badge


def project_row(
    name: str,
    client: str,
    status: str,
    video_count: int,
    on_click=None,
) -> ft.Container:
    """Project list row."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.FOLDER_OUTLINED, size=24, color=COLORS["blue"]),
                    width=48,
                    height=48,
                    bgcolor=COLORS["warm_white"],
                    border_radius=8,
                    alignment=ft.alignment.center,
                ),
                ft.Column(
                    controls=[
                        ft.Text(name, size=16, weight=ft.FontWeight.W_500, color=COLORS["black"]),
                        ft.Text(client, size=14, color=COLORS["steel"]),
                    ],
                    spacing=2,
                    expand=True,
                ),
                ft.Text(f"{video_count} videos", size=14, color=COLORS["steel"]),
                status_badge(status),
                ft.IconButton(
                    icon=ft.Icons.CHEVRON_RIGHT,
                    icon_color=COLORS["steel"],
                    on_click=on_click,
                ),
            ],
            spacing=SPACING["md"],
        ),
        padding=SPACING["sm"],
        on_click=on_click,
        ink=True,
    )


def projects_page(page: ft.Page) -> ft.Control:
    """Build the projects page."""

    # Filter state
    status_filter = ft.Dropdown(
        label="Status",
        width=150,
        options=[
            ft.dropdown.Option("all", "All"),
            ft.dropdown.Option("draft", "Draft"),
            ft.dropdown.Option("in_progress", "In Progress"),
            ft.dropdown.Option("review", "Review"),
            ft.dropdown.Option("approved", "Approved"),
            ft.dropdown.Option("delivered", "Delivered"),
        ],
        value="all",
    )

    return ft.Column(
        controls=[
            page_header(
                title="Projects",
                subtitle="Manage client projects and videos",
                actions=[
                    primary_button(
                        text="New Project",
                        icon=ft.Icons.ADD,
                        on_click=lambda e: None,  # TODO: Open create modal
                    ),
                ],
            ),

            # Filters
            ft.Row(
                controls=[
                    status_filter,
                    ft.Container(expand=True),
                    ft.TextField(
                        hint_text="Search projects...",
                        prefix_icon=ft.Icons.SEARCH,
                        width=300,
                        border_radius=6,
                    ),
                ],
                spacing=SPACING["md"],
            ),

            ft.Container(height=SPACING["md"]),

            # Projects list
            card(
                content=ft.Column(
                    controls=[
                        project_row(
                            name="January Campaign",
                            client="Amsterdam Coffee Roasters",
                            status="in_progress",
                            video_count=4,
                        ),
                        ft.Divider(height=1, color=COLORS["silver"]),
                        project_row(
                            name="Product Launch",
                            client="Tech Gadgets NL",
                            status="review",
                            video_count=8,
                        ),
                        ft.Divider(height=1, color=COLORS["silver"]),
                        project_row(
                            name="Brand Refresh",
                            client="Fitness First Amsterdam",
                            status="approved",
                            video_count=6,
                        ),
                        ft.Divider(height=1, color=COLORS["silver"]),
                        project_row(
                            name="Holiday Campaign",
                            client="Local Bakery",
                            status="delivered",
                            video_count=12,
                        ),
                        ft.Divider(height=1, color=COLORS["silver"]),
                        project_row(
                            name="New Client Onboarding",
                            client="Design Studio",
                            status="draft",
                            video_count=0,
                        ),
                    ],
                ),
                padding=0,
            ),
        ],
    )
