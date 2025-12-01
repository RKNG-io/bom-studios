# BOM Studios Engine

Desktop app for managing video production pipeline. Review drafts, approve videos, track costs.

## Quick Start

```bash
cd engine

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Run the app
python app.py
```

## Features

| Page | Description |
|------|-------------|
| Dashboard | Overview, stats, recent activity |
| Create Video | New video form with all options |
| Projects | Client projects and video counts |
| Library | All videos with filters and search |
| Settings | API keys, preferences |

## Requirements

- Python 3.11+
- Flet 0.24+

## Building Standalone App

To create a standalone executable:

```bash
pip install flet
flet build macos  # or: flet build windows / flet build linux
```

The executable will be in `build/` directory.

## API Connection

The Engine connects to the BOM Studios API for:
- Fetching projects and videos
- Triggering video generation
- Updating video status

Configure the API URL in Settings or via environment variable:

```bash
export BOM_API_URL=https://your-api.ondigitalocean.app
```
