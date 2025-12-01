"""App shell layout with sidebar."""

import flet as ft
from ui.theme import COLORS, SPACING
from ui.components.sidebar import sidebar


def app_shell(page: ft.Page, content: ft.Control) -> ft.Row:
    """Main app layout with sidebar and content area."""
    return ft.Row(
        controls=[
            sidebar(page),
            ft.VerticalDivider(width=1, color=COLORS["silver"]),
            ft.Container(
                content=ft.Column(
                    controls=[content],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                expand=True,
                bgcolor=COLORS["warm_white"],
                padding=SPACING["xl"],
            ),
        ],
        expand=True,
        spacing=0,
    )


def page_header(title: str, subtitle: str = None, actions: list = None) -> ft.Container:
    """Page header with title and optional actions."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            title,
                            size=32,
                            weight=ft.FontWeight.W_500,
                            color=COLORS["black"],
                        ),
                        ft.Text(
                            subtitle,
                            size=16,
                            color=COLORS["steel"],
                        ) if subtitle else ft.Container(),
                    ],
                    spacing=4,
                ),
                ft.Container(expand=True),
                ft.Row(
                    controls=actions or [],
                    spacing=SPACING["sm"],
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.only(bottom=SPACING["lg"]),
    )
