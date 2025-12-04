# SKILL.md — Engine Agent

## Role

Build and maintain the Flet desktop application used internally by Jeroen for video production, project management, and client workflows.

---

## Scope

- `engine/` directory only
- Flet UI components and pages
- Local state management
- Provider integrations (Replicate, ElevenLabs, HeyGen)
- SQLite database operations
- Cost tracking

**Out of scope:** API endpoints, client portal, n8n workflows

---

## Tech Stack

- Python 3.11
- Flet 0.21+
- SQLAlchemy 2.0
- SQLite
- httpx (async HTTP)

---

## Design System Tokens

Apply these consistently across all UI:

```python
# theme.py

COLORS = {
    "black": "#0C0C0C",
    "warm_white": "#FAF9F7",
    "paper_white": "#FFFFFF",
    "slate": "#2E2E2E",
    "steel": "#5A5A5A",
    "silver": "#E8E6E3",
    "blue": "#6B8EA3",
    "sage": "#9BA88A",
    "error": "#D64545",
}

SPACING = {
    "xs": 8,
    "sm": 16,
    "md": 24,
    "lg": 32,
    "xl": 48,
    "2xl": 64,
    "3xl": 96,
}

TYPOGRAPHY = {
    "h1": {"size": 48, "weight": "w500"},
    "h2": {"size": 32, "weight": "w500"},
    "h3": {"size": 24, "weight": "w500"},
    "body": {"size": 16, "weight": "w400"},
    "caption": {"size": 14, "weight": "w400"},
}
```

---

## File Structure

```
engine/
├── app.py                    # Flet entrypoint
├── ui/
│   ├── pages/
│   │   ├── dashboard.py      # Home with stats, tasks, recent
│   │   ├── create_video.py   # Video creation wizard
│   │   ├── projects.py       # Project list and detail
│   │   ├── library.py        # Content library grid
│   │   └── settings.py       # API keys, preferences
│   ├── components/
│   │   ├── sidebar.py        # Navigation sidebar
│   │   ├── button.py         # Primary, secondary, text buttons
│   │   ├── card.py           # Content cards
│   │   ├── input.py          # Text inputs, textareas
│   │   ├── modal.py          # Dialog modals
│   │   ├── video_card.py     # Video thumbnail + actions
│   │   └── cost_badge.py     # API cost display
│   ├── theme.py              # Design tokens
│   └── layout.py             # App shell with sidebar
├── core/
│   ├── models.py             # SQLAlchemy models
│   ├── database.py           # DB session management
│   ├── projects.py           # Project CRUD operations
│   ├── videos.py             # Video CRUD operations
│   └── costs.py              # API usage tracking
└── providers/
    ├── base.py               # Base provider class
    ├── replicate.py          # Image generation
    ├── elevenlabs.py         # Voice generation
    ├── heygen.py             # Avatar generation (Phase 2b)
    └── drive.py              # Google Drive upload
```

---

## Task Queue

### Phase 0 (Foundation)

- [ ] `app.py` — Basic Flet app with window config
- [ ] `ui/theme.py` — Design tokens
- [ ] `ui/layout.py` — Shell with sidebar navigation
- [ ] `ui/components/sidebar.py` — Nav links, active state
- [ ] `ui/components/button.py` — Primary, secondary variants
- [ ] `ui/pages/dashboard.py` — Placeholder with welcome message
- [ ] `ui/pages/create_video.py` — Placeholder
- [ ] `ui/pages/projects.py` — Placeholder
- [ ] `ui/pages/library.py` — Placeholder
- [ ] `ui/pages/settings.py` — Placeholder
- [ ] `core/database.py` — SQLite connection
- [ ] `core/models.py` — Client, Project, Video, Asset, APIUsage

### Phase 1a (Video Flow)

- [ ] `ui/pages/create_video.py` — Step 1: Script input
- [ ] `ui/pages/create_video.py` — Step 2: Image generation UI
- [ ] `ui/pages/create_video.py` — Step 3: Audio upload
- [ ] `ui/pages/create_video.py` — Step 4: Preview
- [ ] `ui/pages/create_video.py` — Step 5: Export
- [ ] `providers/replicate.py` — Flux image generation
- [ ] `core/costs.py` — Log API usage
- [ ] `ui/components/cost_badge.py` — Show cost per action

### Phase 1b (Projects)

- [ ] `ui/pages/projects.py` — List view with status filters
- [ ] `ui/pages/projects.py` — Create project modal
- [ ] `ui/pages/projects.py` — Project detail view
- [ ] `ui/pages/library.py` — Video grid with filters
- [ ] `ui/components/video_card.py` — Thumbnail, status, actions

---

## Component Patterns

### Button

```python
# components/button.py
import flet as ft
from ui.theme import COLORS, SPACING

def primary_button(text: str, on_click, disabled: bool = False) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text=text,
        on_click=on_click,
        disabled=disabled,
        bgcolor=COLORS["black"],
        color=COLORS["paper_white"],
        style=ft.ButtonStyle(
            padding=ft.padding.symmetric(horizontal=SPACING["lg"], vertical=SPACING["sm"]),
            shape=ft.RoundedRectangleBorder(radius=6),
        ),
    )

def secondary_button(text: str, on_click, disabled: bool = False) -> ft.OutlinedButton:
    return ft.OutlinedButton(
        text=text,
        on_click=on_click,
        disabled=disabled,
        style=ft.ButtonStyle(
            color=COLORS["black"],
            padding=ft.padding.symmetric(horizontal=SPACING["lg"], vertical=SPACING["sm"]),
            shape=ft.RoundedRectangleBorder(radius=6),
            side=ft.BorderSide(width=1, color=COLORS["black"]),
        ),
    )
```

### Card

```python
# components/card.py
import flet as ft
from ui.theme import COLORS, SPACING

def card(content: ft.Control, padding: int = SPACING["md"]) -> ft.Container:
    return ft.Container(
        content=content,
        padding=padding,
        bgcolor=COLORS["paper_white"],
        border=ft.border.all(1, COLORS["silver"]),
        border_radius=8,
    )
```

### Layout Shell

```python
# layout.py
import flet as ft
from ui.theme import COLORS
from ui.components.sidebar import sidebar

def app_shell(page: ft.Page, content: ft.Control) -> ft.Row:
    return ft.Row(
        controls=[
            sidebar(page),
            ft.VerticalDivider(width=1, color=COLORS["silver"]),
            ft.Container(
                content=content,
                expand=True,
                bgcolor=COLORS["warm_white"],
                padding=48,
            ),
        ],
        expand=True,
    )
```

---

## Provider Pattern

```python
# providers/base.py
from abc import ABC, abstractmethod
from core.costs import log_api_usage

class BaseProvider(ABC):
    provider_name: str
    
    @abstractmethod
    async def generate(self, **kwargs) -> dict:
        pass
    
    def log_cost(self, action: str, cost_cents: int, project_id: str = None):
        log_api_usage(
            provider=self.provider_name,
            action=action,
            cost_cents=cost_cents,
            project_id=project_id,
        )
```

```python
# providers/replicate.py
import replicate
from providers.base import BaseProvider

class ReplicateProvider(BaseProvider):
    provider_name = "replicate"
    
    async def generate_image(
        self,
        prompt: str,
        aspect_ratio: str = "9:16",
        project_id: str = None,
    ) -> str:
        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={"prompt": prompt, "aspect_ratio": aspect_ratio},
        )
        
        # Flux Schnell: ~$0.003 per image
        self.log_cost("image_gen", cost_cents=0.3, project_id=project_id)
        
        return output[0]  # URL
```

---

## State Management

Use Flet's built-in state with `page.session`:

```python
# Store wizard state
page.session.set("wizard_step", 1)
page.session.set("wizard_data", {
    "script": "",
    "images": [],
    "audio_url": None,
})

# Retrieve
step = page.session.get("wizard_step")
data = page.session.get("wizard_data")
```

For persistent state, write to SQLite immediately.

---

## Error Handling

```python
async def safe_generate(provider, **kwargs):
    try:
        return await provider.generate(**kwargs)
    except Exception as e:
        # Log error
        print(f"Provider error: {e}")
        # Return error state, don't crash
        return {"error": str(e)}
```

Show errors in UI with snackbar:

```python
page.snack_bar = ft.SnackBar(
    content=ft.Text("Image generation failed. Please retry."),
    bgcolor=COLORS["error"],
)
page.snack_bar.open = True
page.update()
```

---

## Testing

```bash
# Run app in debug mode
cd engine && flet run app.py --web

# Test provider directly
python -c "from providers.replicate import ReplicateProvider; ..."
```

---

## Handoff Points

- **To API Agent:** When video needs server-side assembly (FFmpeg), call API endpoint
- **From API Agent:** Receive webhook data (new project from intake form)
- **To Portal Agent:** Video status changes trigger portal updates via API

---

## When Stuck

1. Check Flet docs: https://flet.dev/docs/
2. Check `/docs/bom-studios-engine-spec.md` for feature requirements
3. Check `/docs/bom-studios-design-system.md` for visual specs
4. If provider API unclear, stub the response and continue
