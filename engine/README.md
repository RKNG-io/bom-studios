# BOM Studios Engine

Desktop app for managing video production pipeline. Review drafts, approve videos, track costs.

## Quick Start

```bash
cd engine

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Set API URL
export BOM_API_URL=https://your-api.ondigitalocean.app

# Run the app
python app.py
```

A window will open with your dashboard.

## Features

| Page | Description |
|------|-------------|
| Dashboard | Overview, stats, recent activity from API |
| Create Video | 5-step wizard for video creation |
| Projects | Client projects and video counts |
| Library | All videos with filters and search |
| Settings | API keys, Google Drive, preferences |

## Requirements

- Python 3.11+
- Flet 0.24+

## API Connection

The Engine connects to the BOM Studios API for:
- Fetching clients, projects, and videos
- Creating and managing videos
- Approve/reject workflow

Set the API URL:

```bash
export BOM_API_URL=https://your-api.ondigitalocean.app
```

## Building Standalone App (Optional)

Requires Flutter SDK to be installed first.

```bash
# Install Flutter: https://flutter.dev/docs/get-started/install
flet build macos  # or: flet build windows / flet build linux
```

The executable will be in `build/` directory.
