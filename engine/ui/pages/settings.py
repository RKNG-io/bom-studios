"""Settings page - app configuration."""

import flet as ft
from ui.theme import COLORS, SPACING
from ui.layout import page_header
from ui.components.card import card
from ui.components.button import primary_button, secondary_button
from ui.components.input import text_input


def settings_section(title: str, content: ft.Control) -> ft.Container:
    """Settings section with title."""
    return ft.Column(
        controls=[
            ft.Text(title, size=18, weight=ft.FontWeight.W_500, color=COLORS["black"]),
            ft.Container(height=SPACING["sm"]),
            card(content=content),
        ],
        spacing=0,
    )


def settings_page(page: ft.Page) -> ft.Control:
    """Build the settings page."""
    return ft.Column(
        controls=[
            page_header(
                title="Settings",
                subtitle="Configure your BOM Studios Engine",
            ),

            # API Keys section
            settings_section(
                title="API Keys",
                content=ft.Column(
                    controls=[
                        text_input(
                            label="Replicate API Token",
                            hint="r8_...",
                            password=True,
                        ),
                        ft.Container(height=SPACING["sm"]),
                        text_input(
                            label="ElevenLabs API Key",
                            password=True,
                        ),
                        ft.Container(height=SPACING["sm"]),
                        text_input(
                            label="Anthropic API Key",
                            hint="sk-ant-...",
                            password=True,
                        ),
                        ft.Container(height=SPACING["sm"]),
                        text_input(
                            label="HeyGen API Key (Optional)",
                            password=True,
                        ),
                        ft.Container(height=SPACING["md"]),
                        primary_button(text="Save API Keys"),
                    ],
                ),
            ),

            ft.Container(height=SPACING["lg"]),

            # Google Drive section
            settings_section(
                title="Google Drive",
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.CLOUD_OFF, color=COLORS["steel"]),
                                ft.Text("Not connected", color=COLORS["steel"]),
                            ],
                            spacing=SPACING["xs"],
                        ),
                        ft.Container(height=SPACING["sm"]),
                        secondary_button(
                            text="Connect Google Drive",
                            icon=ft.Icons.LINK,
                        ),
                    ],
                ),
            ),

            ft.Container(height=SPACING["lg"]),

            # Defaults section
            settings_section(
                title="Default Settings",
                content=ft.Column(
                    controls=[
                        ft.Dropdown(
                            label="Default Voice",
                            width=300,
                            options=[
                                ft.dropdown.Option("dutch_male", "Dutch Male"),
                                ft.dropdown.Option("dutch_female", "Dutch Female"),
                                ft.dropdown.Option("english_male", "English Male"),
                                ft.dropdown.Option("english_female", "English Female"),
                            ],
                            value="dutch_male",
                        ),
                        ft.Container(height=SPACING["sm"]),
                        ft.Dropdown(
                            label="Default Video Format",
                            width=300,
                            options=[
                                ft.dropdown.Option("vertical", "Vertical (9:16)"),
                                ft.dropdown.Option("square", "Square (1:1)"),
                                ft.dropdown.Option("horizontal", "Horizontal (16:9)"),
                            ],
                            value="vertical",
                        ),
                        ft.Container(height=SPACING["md"]),
                        primary_button(text="Save Defaults"),
                    ],
                ),
            ),

            ft.Container(height=SPACING["lg"]),

            # About section
            settings_section(
                title="About",
                content=ft.Column(
                    controls=[
                        ft.Text("BOM Studios Engine", size=16, weight=ft.FontWeight.W_500),
                        ft.Text("Version 0.1.0", size=14, color=COLORS["steel"]),
                        ft.Container(height=SPACING["sm"]),
                        ft.Text(
                            "Internal video production tool for BOM Studios.",
                            size=14,
                            color=COLORS["steel"],
                        ),
                    ],
                ),
            ),
        ],
    )
