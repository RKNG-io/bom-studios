"""Button components."""

import flet as ft
from ui.theme import COLORS, SPACING


def primary_button(
    text: str,
    on_click=None,
    disabled: bool = False,
    icon: str = None,
    expand: bool = False,
) -> ft.ElevatedButton:
    """Primary action button - black background, white text."""
    return ft.ElevatedButton(
        text=text,
        on_click=on_click,
        disabled=disabled,
        icon=icon,
        bgcolor=COLORS["black"],
        color=COLORS["paper_white"],
        expand=expand,
        style=ft.ButtonStyle(
            padding=ft.padding.symmetric(horizontal=SPACING["lg"], vertical=SPACING["sm"]),
            shape=ft.RoundedRectangleBorder(radius=6),
        ),
    )


def secondary_button(
    text: str,
    on_click=None,
    disabled: bool = False,
    icon: str = None,
    expand: bool = False,
) -> ft.OutlinedButton:
    """Secondary action button - outlined."""
    return ft.OutlinedButton(
        text=text,
        on_click=on_click,
        disabled=disabled,
        icon=icon,
        expand=expand,
        style=ft.ButtonStyle(
            color=COLORS["black"],
            padding=ft.padding.symmetric(horizontal=SPACING["lg"], vertical=SPACING["sm"]),
            shape=ft.RoundedRectangleBorder(radius=6),
            side=ft.BorderSide(width=1, color=COLORS["black"]),
        ),
    )


def text_button(
    text: str,
    on_click=None,
    disabled: bool = False,
    icon: str = None,
) -> ft.TextButton:
    """Text-only button for tertiary actions."""
    return ft.TextButton(
        text=text,
        on_click=on_click,
        disabled=disabled,
        icon=icon,
        style=ft.ButtonStyle(
            color=COLORS["blue"],
            padding=ft.padding.symmetric(horizontal=SPACING["sm"], vertical=SPACING["xs"]),
        ),
    )
