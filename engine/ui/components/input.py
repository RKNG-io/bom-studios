"""Input components."""

import flet as ft
from ui.theme import COLORS, SPACING


def text_input(
    label: str = None,
    hint: str = None,
    value: str = "",
    on_change=None,
    password: bool = False,
    multiline: bool = False,
    expand: bool = False,
) -> ft.TextField:
    """Styled text input."""
    return ft.TextField(
        label=label,
        hint_text=hint,
        value=value,
        on_change=on_change,
        password=password,
        multiline=multiline,
        expand=expand,
        border_color=COLORS["silver"],
        focused_border_color=COLORS["black"],
        cursor_color=COLORS["black"],
        text_size=16,
        border_radius=6,
        content_padding=SPACING["sm"],
    )


def text_area(
    label: str = None,
    hint: str = None,
    value: str = "",
    on_change=None,
    min_lines: int = 3,
    max_lines: int = 10,
    expand: bool = False,
) -> ft.TextField:
    """Multiline text area."""
    return ft.TextField(
        label=label,
        hint_text=hint,
        value=value,
        on_change=on_change,
        multiline=True,
        min_lines=min_lines,
        max_lines=max_lines,
        expand=expand,
        border_color=COLORS["silver"],
        focused_border_color=COLORS["black"],
        cursor_color=COLORS["black"],
        text_size=16,
        border_radius=6,
        content_padding=SPACING["sm"],
    )
