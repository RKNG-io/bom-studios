"""Card component."""

import flet as ft
from ui.theme import COLORS, SPACING


def card(
    content: ft.Control,
    padding: int = None,
    on_click=None,
    elevated: bool = False,
) -> ft.Container:
    """Content card with optional click handler."""
    if padding is None:
        padding = SPACING["md"]

    return ft.Container(
        content=content,
        padding=padding,
        bgcolor=COLORS["paper_white"],
        border=ft.border.all(1, COLORS["silver"]),
        border_radius=8,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.colors.with_opacity(0.06, ft.colors.BLACK),
        ) if elevated else None,
        on_click=on_click,
        ink=on_click is not None,
    )
