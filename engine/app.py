"""BOM Studios Engine - Desktop video production app."""

import flet as ft
from ui.theme import COLORS
from ui.layout import app_shell
from ui.pages import (
    dashboard_page,
    create_video_page,
    projects_page,
    library_page,
    settings_page,
)


def main(page: ft.Page):
    """Main entry point for the Flet app."""

    # Window configuration
    page.title = "BOM Studios Engine"
    page.window.width = 1400
    page.window.height = 900
    page.window.min_width = 1000
    page.window.min_height = 700
    page.bgcolor = COLORS["warm_white"]
    page.padding = 0

    # Route handling
    def route_change(e):
        page.views.clear()

        # Get content based on route
        route = page.route or "/"

        if route == "/":
            content = dashboard_page(page)
        elif route == "/create":
            content = create_video_page(page)
        elif route == "/projects":
            content = projects_page(page)
        elif route == "/library":
            content = library_page(page)
        elif route == "/settings":
            content = settings_page(page)
        else:
            content = dashboard_page(page)

        # Wrap in app shell
        page.views.append(
            ft.View(
                route=route,
                controls=[app_shell(page, content)],
                padding=0,
                bgcolor=COLORS["warm_white"],
            )
        )

        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Navigate to initial route
    page.go(page.route or "/")


if __name__ == "__main__":
    ft.app(target=main)
