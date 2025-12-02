"""Projects page - list and manage projects."""

import flet as ft
from ui.theme import COLORS, SPACING
from ui.layout import page_header
from ui.components.card import card
from ui.components.button import primary_button, secondary_button
from ui.components.status_badge import status_badge
from core.api import api


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

    # Fetch projects from API
    projects = api.get_projects()

    # Build project rows
    project_controls = []
    for i, project in enumerate(projects):
        if i > 0:
            project_controls.append(ft.Divider(height=1, color=COLORS["silver"]))
        project_controls.append(
            project_row(
                name=project.get("name", "Untitled Project"),
                client=project.get("client_name", "Unknown Client"),
                status=project.get("status", "draft"),
                video_count=project.get("video_count", 0),
            )
        )

    # Fallback if no projects
    if not project_controls:
        project_controls = [
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.FOLDER_OFF_OUTLINED, size=48, color=COLORS["steel"]),
                        ft.Text("No projects yet", color=COLORS["steel"]),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=SPACING["sm"],
                ),
                padding=SPACING["xl"],
                alignment=ft.alignment.center,
            )
        ]

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
                content=ft.Column(controls=project_controls),
                padding=0,
            ),
        ],
    )
