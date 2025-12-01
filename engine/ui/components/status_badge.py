"""Status badge component."""

import flet as ft
from ui.theme import COLORS


STATUS_COLORS = {
    "draft": {"bg": COLORS["silver"], "text": COLORS["slate"]},
    "scripting": {"bg": "#E3F2FD", "text": "#1565C0"},
    "generating": {"bg": "#FFF3E0", "text": "#E65100"},
    "rendering": {"bg": "#FFF3E0", "text": "#E65100"},
    "review": {"bg": "#F3E5F5", "text": "#7B1FA2"},
    "approved": {"bg": "#E8F5E9", "text": "#2E7D32"},
    "delivered": {"bg": COLORS["sage"], "text": COLORS["paper_white"]},
    "in_progress": {"bg": "#FFF3E0", "text": "#E65100"},
}


def status_badge(status: str) -> ft.Container:
    """Status indicator badge."""
    colors = STATUS_COLORS.get(status, STATUS_COLORS["draft"])

    return ft.Container(
        content=ft.Text(
            status.replace("_", " ").title(),
            size=12,
            weight=ft.FontWeight.W_500,
            color=colors["text"],
        ),
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
        bgcolor=colors["bg"],
        border_radius=4,
    )
