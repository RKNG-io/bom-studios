"""Video card component."""

import flet as ft
from ui.theme import COLORS, SPACING
from ui.components.status_badge import status_badge


def video_card(
    title: str,
    status: str,
    thumbnail_url: str = None,
    on_click=None,
) -> ft.Container:
    """Video card with thumbnail, title, and status."""
    return ft.Container(
        content=ft.Column(
            controls=[
                # Thumbnail
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.PLAY_CIRCLE_OUTLINE,
                        size=40,
                        color=COLORS["steel"],
                    ) if not thumbnail_url else ft.Image(
                        src=thumbnail_url,
                        fit=ft.ImageFit.COVER,
                        width=200,
                        height=356,  # 9:16 aspect ratio
                    ),
                    width=200,
                    height=200,
                    bgcolor=COLORS["silver"],
                    border_radius=6,
                    alignment=ft.alignment.center,
                ),
                # Title
                ft.Text(
                    title,
                    size=14,
                    weight=ft.FontWeight.W_500,
                    color=COLORS["black"],
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                # Status
                status_badge(status),
            ],
            spacing=SPACING["xs"],
        ),
        padding=SPACING["sm"],
        bgcolor=COLORS["paper_white"],
        border=ft.border.all(1, COLORS["silver"]),
        border_radius=8,
        on_click=on_click,
        ink=on_click is not None,
        width=232,
    )
