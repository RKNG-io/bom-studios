"""Navigation sidebar."""

import flet as ft
from ui.theme import COLORS, SPACING, SIDEBAR_WIDTH


def nav_item(page: ft.Page, icon: str, label: str, route: str, selected: bool = False) -> ft.Container:
    """Navigation item with icon and label."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(
                    icon,
                    size=20,
                    color=COLORS["black"] if selected else COLORS["steel"],
                ),
                ft.Text(
                    label,
                    size=14,
                    weight=ft.FontWeight.W_500 if selected else ft.FontWeight.W_400,
                    color=COLORS["black"] if selected else COLORS["steel"],
                ),
            ],
            spacing=SPACING["sm"],
        ),
        padding=ft.padding.symmetric(horizontal=SPACING["sm"], vertical=SPACING["xs"] + 4),
        border_radius=6,
        bgcolor=COLORS["silver"] if selected else None,
        on_click=lambda e: page.go(route),
        ink=True,
    )


def sidebar(page: ft.Page) -> ft.Container:
    """Navigation sidebar with logo and nav items."""
    current_route = page.route or "/"

    nav_items_data = [
        {"icon": ft.Icons.DASHBOARD_OUTLINED, "label": "Dashboard", "route": "/"},
        {"icon": ft.Icons.ADD_CIRCLE_OUTLINE, "label": "Create Video", "route": "/create"},
        {"icon": ft.Icons.FOLDER_OUTLINED, "label": "Projects", "route": "/projects"},
        {"icon": ft.Icons.VIDEO_LIBRARY_OUTLINED, "label": "Library", "route": "/library"},
        {"icon": ft.Icons.SETTINGS_OUTLINED, "label": "Settings", "route": "/settings"},
    ]

    return ft.Container(
        width=SIDEBAR_WIDTH,
        bgcolor=COLORS["paper_white"],
        padding=SPACING["md"],
        content=ft.Column(
            controls=[
                # Logo
                ft.Container(
                    content=ft.Text(
                        "BOM",
                        size=24,
                        weight=ft.FontWeight.W_500,
                        color=COLORS["black"],
                    ),
                    padding=ft.padding.only(bottom=SPACING["xl"]),
                ),
                # Nav items
                ft.Column(
                    controls=[
                        nav_item(
                            page=page,
                            icon=item["icon"],
                            label=item["label"],
                            route=item["route"],
                            selected=current_route == item["route"],
                        )
                        for item in nav_items_data
                    ],
                    spacing=4,
                ),
                # Spacer
                ft.Container(expand=True),
                # Cost summary
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "API Spend",
                                size=12,
                                color=COLORS["steel"],
                            ),
                            ft.Text(
                                "€0.00 this month",
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color=COLORS["black"],
                            ),
                        ],
                        spacing=4,
                    ),
                    padding=SPACING["sm"],
                    bgcolor=COLORS["warm_white"],
                    border_radius=6,
                ),
            ],
            expand=True,
        ),
    )
