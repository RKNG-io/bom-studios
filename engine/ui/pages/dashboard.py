"""Dashboard page - home view with stats and recent activity."""

import flet as ft
from ui.theme import COLORS, SPACING
from ui.layout import page_header
from ui.components.card import card
from ui.components.button import primary_button
from ui.components.status_badge import status_badge
from core.api import api


def stat_card(label: str, value: str, icon: str) -> ft.Container:
    """Stat card for dashboard metrics."""
    return card(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(icon, size=24, color=COLORS["blue"]),
                    padding=SPACING["sm"],
                    bgcolor=COLORS["warm_white"],
                    border_radius=8,
                ),
                ft.Column(
                    controls=[
                        ft.Text(value, size=24, weight=ft.FontWeight.W_500, color=COLORS["black"]),
                        ft.Text(label, size=14, color=COLORS["steel"]),
                    ],
                    spacing=2,
                ),
            ],
            spacing=SPACING["md"],
        ),
    )


def recent_video_row(title: str, status: str, date: str) -> ft.Container:
    """Row for recent videos list."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.PLAY_CIRCLE_OUTLINE, size=20, color=COLORS["steel"]),
                    width=40,
                    height=40,
                    bgcolor=COLORS["silver"],
                    border_radius=6,
                    alignment=ft.alignment.center,
                ),
                ft.Column(
                    controls=[
                        ft.Text(title, size=14, weight=ft.FontWeight.W_500, color=COLORS["black"]),
                        ft.Text(date, size=12, color=COLORS["steel"]),
                    ],
                    spacing=2,
                    expand=True,
                ),
                status_badge(status),
            ],
            spacing=SPACING["sm"],
        ),
        padding=ft.padding.symmetric(vertical=SPACING["xs"]),
    )


def dashboard_page(page: ft.Page) -> ft.Control:
    """Build the dashboard page."""

    # Fetch data from API
    projects = api.get_projects()
    videos = api.get_videos()
    clients = api.get_clients()

    # Calculate stats
    video_count = len(videos)
    pending_count = len([v for v in videos if v.get("status") in ["pending_review", "pending_client", "review"]])
    client_count = len(clients)

    # Get recent videos (last 4)
    recent_videos = sorted(videos, key=lambda v: v.get("created_at", ""), reverse=True)[:4]

    # Build recent videos list
    recent_controls = []
    for i, video in enumerate(recent_videos):
        if i > 0:
            recent_controls.append(ft.Divider(height=1, color=COLORS["silver"]))
        recent_controls.append(
            recent_video_row(
                video.get("title", "Untitled"),
                video.get("status", "draft"),
                video.get("created_at", "")[:10] if video.get("created_at") else "Unknown",
            )
        )

    # Fallback if no videos
    if not recent_controls:
        recent_controls = [
            ft.Container(
                content=ft.Text("No videos yet", color=COLORS["steel"]),
                padding=SPACING["lg"],
                alignment=ft.alignment.center,
            )
        ]

    return ft.Column(
        controls=[
            # Header
            page_header(
                title="Dashboard",
                subtitle="Welcome back, Jeroen",
                actions=[
                    primary_button(
                        text="Create Video",
                        icon=ft.Icons.ADD,
                        on_click=lambda e: page.go("/create"),
                    ),
                ],
            ),

            # Stats row
            ft.Row(
                controls=[
                    stat_card("Videos This Month", str(video_count), ft.Icons.VIDEO_LIBRARY_OUTLINED),
                    stat_card("Pending Review", str(pending_count), ft.Icons.PENDING_ACTIONS_OUTLINED),
                    stat_card("Active Clients", str(client_count), ft.Icons.PEOPLE_OUTLINE),
                    stat_card("API Spend", "€0.00", ft.Icons.EURO_OUTLINED),
                ],
                spacing=SPACING["md"],
                wrap=True,
            ),

            ft.Container(height=SPACING["lg"]),

            # Recent videos section
            ft.Row(
                controls=[
                    # Recent videos
                    ft.Container(
                        content=card(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Recent Videos",
                                        size=18,
                                        weight=ft.FontWeight.W_500,
                                        color=COLORS["black"],
                                    ),
                                    ft.Container(height=SPACING["sm"]),
                                    *recent_controls,
                                ],
                            ),
                        ),
                        expand=2,
                    ),

                    # Quick actions
                    ft.Container(
                        content=card(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Quick Actions",
                                        size=18,
                                        weight=ft.FontWeight.W_500,
                                        color=COLORS["black"],
                                    ),
                                    ft.Container(height=SPACING["sm"]),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, color=COLORS["black"]),
                                        title=ft.Text("Create new video"),
                                        on_click=lambda e: page.go("/create"),
                                    ),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.Icons.FOLDER_OPEN_OUTLINED, color=COLORS["black"]),
                                        title=ft.Text("View all projects"),
                                        on_click=lambda e: page.go("/projects"),
                                    ),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.Icons.PENDING_ACTIONS_OUTLINED, color=COLORS["black"]),
                                        title=ft.Text("Review pending videos"),
                                        on_click=lambda e: page.go("/library"),
                                    ),
                                ],
                            ),
                        ),
                        expand=1,
                    ),
                ],
                spacing=SPACING["md"],
            ),
        ],
        spacing=0,
    )
