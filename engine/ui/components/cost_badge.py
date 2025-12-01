"""Cost badge component."""

import flet as ft
from ui.theme import COLORS


def cost_badge(cost_cents: int) -> ft.Container:
    """Display API cost in euros."""
    cost_euros = cost_cents / 100

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.EURO_OUTLINED,
                    size=14,
                    color=COLORS["steel"],
                ),
                ft.Text(
                    f"{cost_euros:.2f}",
                    size=12,
                    color=COLORS["steel"],
                ),
            ],
            spacing=4,
            tight=True,
        ),
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
        bgcolor=COLORS["warm_white"],
        border_radius=4,
    )
