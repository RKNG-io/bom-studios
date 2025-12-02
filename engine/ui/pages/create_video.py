"""Create video page - intake wizard matching website flow."""

import flet as ft
from ui.theme import COLORS, SPACING
from ui.layout import page_header
from ui.components.card import card
from ui.components.button import primary_button, secondary_button
from ui.components.input import text_area, text_input
from core.api import api_client


def _build_progress(step: int, total: int = 4) -> ft.Container:
    """Progress bar matching website style."""
    bars = []
    for i in range(total):
        bars.append(
            ft.Container(
                expand=True,
                height=4,
                bgcolor=COLORS["black"] if i < step else COLORS["silver"],
                border_radius=2,
            )
        )

    return ft.Container(
        content=ft.Row(controls=bars, spacing=8),
        margin=ft.margin.only(bottom=SPACING["lg"]),
    )


def _step_business(data: dict, update_field) -> ft.Container:
    """Step 1: About Your Business."""
    return card(
        content=ft.Column(
            controls=[
                ft.Text(
                    "About Your Business",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color=COLORS["black"],
                ),
                ft.Container(height=SPACING["md"]),
                text_input(
                    label="What's your business called?",
                    hint="e.g. Amsterdam Coffee Roasters",
                    value=data.get("business_name", ""),
                    on_change=lambda e: update_field("business_name", e.control.value),
                ),
                ft.Container(height=SPACING["sm"]),
                text_input(
                    label="Client email address",
                    hint="client@business.com",
                    value=data.get("email", ""),
                    on_change=lambda e: update_field("email", e.control.value),
                ),
                ft.Text(
                    "We'll send the video here.",
                    size=12,
                    color=COLORS["steel"],
                ),
                ft.Container(height=SPACING["sm"]),
                text_area(
                    label="Website and social links",
                    hint="https://business.com\ninstagram.com/business\nlinkedin.com/company/business",
                    value=data.get("links", ""),
                    min_lines=3,
                    max_lines=5,
                    on_change=lambda e: update_field("links", e.control.value),
                ),
                ft.Text(
                    "One per line. Helps us understand the brand quickly.",
                    size=12,
                    color=COLORS["steel"],
                ),
            ],
        ),
        padding=SPACING["lg"],
    )


def _step_context(data: dict, update_field) -> ft.Container:
    """Step 2: What You Do."""
    return card(
        content=ft.Column(
            controls=[
                ft.Text(
                    "What They Do",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color=COLORS["black"],
                ),
                ft.Container(height=SPACING["md"]),
                text_area(
                    label="What do they sell or offer?",
                    hint="e.g. We sell specialty coffee beans, roasted weekly and delivered to your door.",
                    value=data.get("what_they_sell", ""),
                    min_lines=3,
                    max_lines=5,
                    on_change=lambda e: update_field("what_they_sell", e.control.value),
                ),
                ft.Text(
                    "Be specific. What would they tell someone at a party?",
                    size=12,
                    color=COLORS["steel"],
                ),
                ft.Container(height=SPACING["sm"]),
                text_area(
                    label="Who buys from them?",
                    hint="e.g. Coffee lovers who brew at home and care about quality.",
                    value=data.get("target_customer", ""),
                    min_lines=3,
                    max_lines=5,
                    on_change=lambda e: update_field("target_customer", e.control.value),
                ),
                ft.Text(
                    "Think about their best customers.",
                    size=12,
                    color=COLORS["steel"],
                ),
                ft.Container(height=SPACING["sm"]),
                text_area(
                    label="What makes them different from competitors?",
                    hint="e.g. We roast every week — most supermarket coffee was roasted months ago.",
                    value=data.get("what_makes_different", ""),
                    min_lines=3,
                    max_lines=5,
                    on_change=lambda e: update_field("what_makes_different", e.control.value),
                ),
                ft.Text(
                    "Why should someone choose them?",
                    size=12,
                    color=COLORS["steel"],
                ),
            ],
        ),
        padding=SPACING["lg"],
    )


def _step_prefs(data: dict, update_field, page: ft.Page) -> ft.Container:
    """Step 3: Video Preferences."""

    def make_style_option(value: str, label: str, desc: str) -> ft.Container:
        is_selected = data.get("video_style") == value
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Radio(value=value, fill_color=COLORS["black"]),
                    ft.Column(
                        controls=[
                            ft.Text(label, weight=ft.FontWeight.W_500, color=COLORS["black"]),
                            ft.Text(desc, size=12, color=COLORS["steel"]),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                ],
                spacing=SPACING["sm"],
            ),
            padding=12,
            border=ft.border.all(2, COLORS["black"] if is_selected else COLORS["silver"]),
            border_radius=8,
            bgcolor=COLORS["warm_white"] if is_selected else COLORS["paper_white"],
        )

    def make_length_option(value: str, label: str, desc: str) -> ft.Container:
        is_selected = data.get("video_length") == value
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Radio(value=value, fill_color=COLORS["black"]),
                    ft.Text(label, weight=ft.FontWeight.W_700, size=18, color=COLORS["black"]),
                    ft.Text(desc, size=12, color=COLORS["steel"]),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            padding=12,
            border=ft.border.all(2, COLORS["black"] if is_selected else COLORS["silver"]),
            border_radius=8,
            bgcolor=COLORS["warm_white"] if is_selected else COLORS["paper_white"],
            expand=True,
        )

    def on_style_change(e):
        update_field("video_style", e.control.value)
        page.update()

    def on_length_change(e):
        update_field("video_length", e.control.value)
        page.update()

    return card(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Video Preferences",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color=COLORS["black"],
                ),
                ft.Container(height=SPACING["md"]),
                # Language dropdown
                ft.Text("What language should the video be in?", size=14, weight=ft.FontWeight.W_500),
                ft.Dropdown(
                    value=data.get("language", ""),
                    hint_text="Select a language...",
                    options=[
                        ft.dropdown.Option("nl", "Dutch"),
                        ft.dropdown.Option("en", "English"),
                        ft.dropdown.Option("nl+en", "Dutch + English"),
                    ],
                    on_change=lambda e: update_field("language", e.control.value),
                    border_color=COLORS["silver"],
                    focused_border_color=COLORS["black"],
                    width=300,
                ),
                ft.Container(height=SPACING["md"]),
                # Video style
                ft.Text("What video style fits their product?", size=14, weight=ft.FontWeight.W_500),
                ft.RadioGroup(
                    value=data.get("video_style", ""),
                    on_change=on_style_change,
                    content=ft.Column(
                        controls=[
                            make_style_option("presenter", "Presenter to Camera", "Trust and directness. Good for services."),
                            make_style_option("product", "Product Showcase", "Fast cuts, bold visuals. Built for e-commerce."),
                            make_style_option("animated", "Animated Explainer", "Clean and clear. Works for apps, tools, SaaS."),
                            make_style_option("voiceover", "Voiceover + B-roll", "Professional tone without on-camera talent."),
                            make_style_option("hybrid", "Hybrid", "Mix formats. Test what converts."),
                        ],
                        spacing=8,
                    ),
                ),
                ft.Container(height=SPACING["md"]),
                # Video length
                ft.Text("How long should the video be?", size=14, weight=ft.FontWeight.W_500),
                ft.RadioGroup(
                    value=data.get("video_length", ""),
                    on_change=on_length_change,
                    content=ft.Row(
                        controls=[
                            make_length_option("6s", "6s", "Quick teaser"),
                            make_length_option("15s", "15s", "Most popular"),
                            make_length_option("30s", "30s", "Full story"),
                        ],
                        spacing=12,
                    ),
                ),
                ft.Container(height=SPACING["md"]),
                # Topic
                text_area(
                    label="Any specific topic for this video?",
                    hint="e.g. Our new summer menu, Why our delivery is faster, Meet the team",
                    value=data.get("topic", ""),
                    min_lines=2,
                    max_lines=4,
                    on_change=lambda e: update_field("topic", e.control.value),
                ),
                ft.Text(
                    "Leave blank and we'll suggest something based on their business.",
                    size=12,
                    color=COLORS["steel"],
                ),
            ],
        ),
        padding=SPACING["lg"],
    )


def _step_extras(data: dict, update_field) -> ft.Container:
    """Step 4: Extras (Optional)."""
    return card(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Extras (Optional)",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color=COLORS["black"],
                ),
                ft.Container(height=SPACING["md"]),
                text_area(
                    label="Any videos they like the style of?",
                    hint="Paste links to Instagram Reels, TikToks, or YouTube Shorts they like",
                    value=data.get("reference_videos", ""),
                    min_lines=3,
                    max_lines=5,
                    on_change=lambda e: update_field("reference_videos", e.control.value),
                ),
                ft.Text(
                    "Helps us match their taste.",
                    size=12,
                    color=COLORS["steel"],
                ),
                ft.Container(height=SPACING["sm"]),
                text_area(
                    label="Anything else we should know?",
                    hint="Special offers, brand guidelines, things to avoid...",
                    value=data.get("notes", ""),
                    min_lines=3,
                    max_lines=5,
                    on_change=lambda e: update_field("notes", e.control.value),
                ),
            ],
        ),
        padding=SPACING["lg"],
    )


def _step_submitting() -> ft.Container:
    """Submission in progress state."""
    return card(
        content=ft.Column(
            controls=[
                ft.ProgressRing(color=COLORS["black"]),
                ft.Container(height=SPACING["md"]),
                ft.Text(
                    "Starting video generation...",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color=COLORS["black"],
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "This will create the client, project, and queue the automation pipeline.",
                    size=14,
                    color=COLORS["steel"],
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=SPACING["sm"],
        ),
        padding=SPACING["xl"],
    )


def _step_success() -> ft.Container:
    """Success state after submission."""
    return card(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.CHECK_CIRCLE, size=64, color=COLORS["sage"]),
                ft.Container(height=SPACING["md"]),
                ft.Text(
                    "Video Generation Queued!",
                    size=24,
                    weight=ft.FontWeight.W_600,
                    color=COLORS["black"],
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "The automation pipeline is now running.\nCheck the Library page for progress.",
                    size=14,
                    color=COLORS["steel"],
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=SPACING["sm"],
        ),
        padding=SPACING["xl"],
    )


def _step_error(error_msg: str) -> ft.Container:
    """Error state."""
    return card(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.ERROR_OUTLINE, size=64, color="#D32F2F"),
                ft.Container(height=SPACING["md"]),
                ft.Text(
                    "Submission Failed",
                    size=24,
                    weight=ft.FontWeight.W_600,
                    color=COLORS["black"],
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    error_msg,
                    size=14,
                    color=COLORS["steel"],
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=SPACING["sm"],
        ),
        padding=SPACING["xl"],
    )


def create_video_page(page: ft.Page) -> ft.Control:
    """Build the create video page with intake wizard."""
    # Get or initialize wizard state
    step = page.session.get("wizard_step") or 1
    data = page.session.get("wizard_data") or {}
    status = page.session.get("wizard_status") or "editing"  # editing, submitting, success, error
    error_msg = page.session.get("wizard_error") or ""

    def update_field(field: str, value: str):
        current_data = page.session.get("wizard_data") or {}
        current_data[field] = value
        page.session.set("wizard_data", current_data)

    def can_proceed() -> bool:
        d = page.session.get("wizard_data") or {}
        if step == 1:
            return bool(d.get("business_name", "").strip() and d.get("email", "").strip())
        elif step == 2:
            return bool(
                d.get("what_they_sell", "").strip()
                and d.get("target_customer", "").strip()
                and d.get("what_makes_different", "").strip()
            )
        elif step == 3:
            return bool(
                d.get("language", "").strip()
                and d.get("video_style", "").strip()
                and d.get("video_length", "").strip()
            )
        return True  # Step 4 is all optional

    async def submit_form():
        page.session.set("wizard_status", "submitting")
        page.go("/create")

        d = page.session.get("wizard_data") or {}

        # Build Tally-compatible payload
        payload = {
            "eventId": f"engine-{page.session_id}",
            "eventType": "FORM_RESPONSE",
            "createdAt": "",
            "data": {
                "fields": [
                    {"key": "business_name", "label": "Business Name", "value": d.get("business_name", "")},
                    {"key": "email", "label": "Email", "value": d.get("email", "")},
                    {"key": "links", "label": "Links", "value": d.get("links", "")},
                    {"key": "what_they_sell", "label": "What they sell", "value": d.get("what_they_sell", "")},
                    {"key": "target_customer", "label": "Target Customer", "value": d.get("target_customer", "")},
                    {"key": "what_makes_different", "label": "What makes different", "value": d.get("what_makes_different", "")},
                    {"key": "language", "label": "Language", "value": d.get("language", "en")},
                    {"key": "video_style", "label": "Video Style", "value": d.get("video_style", "")},
                    {"key": "video_length", "label": "Video Length", "value": d.get("video_length", "")},
                    {"key": "topic", "label": "Topic", "value": d.get("topic", "")},
                    {"key": "reference_videos", "label": "Reference Videos", "value": d.get("reference_videos", "")},
                    {"key": "notes", "label": "Notes", "value": d.get("notes", "")},
                ],
            },
        }

        try:
            result = await api_client.post("/webhooks/tally", payload)
            if result.get("status") == "accepted":
                page.session.set("wizard_status", "success")
            else:
                page.session.set("wizard_status", "error")
                page.session.set("wizard_error", result.get("message", "Unknown error"))
        except Exception as e:
            page.session.set("wizard_status", "error")
            page.session.set("wizard_error", str(e))

        page.go("/create")

    def next_step(e):
        current = page.session.get("wizard_step") or 1
        if current < 4:
            page.session.set("wizard_step", current + 1)
            page.go("/create")
        else:
            # Submit on step 4
            page.run_task(submit_form)

    def prev_step(e):
        current = page.session.get("wizard_step") or 1
        if current > 1:
            page.session.set("wizard_step", current - 1)
            page.go("/create")

    def reset_wizard(e):
        page.session.set("wizard_step", 1)
        page.session.set("wizard_data", {})
        page.session.set("wizard_status", "editing")
        page.session.set("wizard_error", "")
        page.go("/create")

    # Build step content based on status
    if status == "submitting":
        step_content = _step_submitting()
        nav_row = ft.Container()  # No navigation while submitting
    elif status == "success":
        step_content = _step_success()
        nav_row = ft.Row(
            controls=[
                ft.Container(expand=True),
                primary_button(text="Create Another", on_click=reset_wizard),
                secondary_button(text="View Library", on_click=lambda e: page.go("/library")),
            ],
            spacing=SPACING["md"],
        )
    elif status == "error":
        step_content = _step_error(error_msg)
        nav_row = ft.Row(
            controls=[
                secondary_button(text="Try Again", on_click=lambda e: page.session.set("wizard_status", "editing") or page.go("/create")),
                ft.Container(expand=True),
            ],
        )
    else:
        # Normal editing mode
        if step == 1:
            step_content = _step_business(data, update_field)
        elif step == 2:
            step_content = _step_context(data, update_field)
        elif step == 3:
            step_content = _step_prefs(data, update_field, page)
        else:
            step_content = _step_extras(data, update_field)

        nav_row = ft.Row(
            controls=[
                secondary_button(text="Back", on_click=prev_step) if step > 1 else ft.Container(),
                ft.Container(expand=True),
                primary_button(
                    text="Next" if step < 4 else "Generate Video",
                    on_click=next_step,
                    disabled=not can_proceed(),
                ),
            ],
        )

    return ft.Column(
        controls=[
            page_header(
                title="Create Video",
                subtitle="Intake wizard — mirrors client journey",
            ),
            _build_progress(step) if status == "editing" else ft.Container(),
            ft.Text(f"Step {step} of 4", size=14, color=COLORS["steel"]) if status == "editing" else ft.Container(),
            ft.Container(height=SPACING["md"]),
            step_content,
            ft.Container(height=SPACING["lg"]),
            nav_row,
        ],
    )
