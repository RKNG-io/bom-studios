"""API client for BOM Studios backend."""

import os
import httpx
from typing import Optional

API_URL = os.getenv("BOM_API_URL", "https://bom-studios-api.ondigitalocean.app")


class APIClient:
    """HTTP client for BOM Studios API."""

    def __init__(self, base_url: str = None, token: str = None):
        self.base_url = base_url or API_URL
        self.token = token
        self._client = httpx.Client(timeout=30.0)

    def _headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def set_token(self, token: str):
        """Set auth token after login."""
        self.token = token

    # Health
    def health(self) -> dict:
        """Check API health."""
        try:
            r = self._client.get(f"{self.base_url}/health")
            return r.json() if r.status_code == 200 else {"status": "error"}
        except Exception:
            return {"status": "offline"}

    # Auth
    def request_magic_link(self, email: str) -> bool:
        """Request magic link login."""
        try:
            r = self._client.post(
                f"{self.base_url}/api/auth/magic-link",
                json={"email": email},
                headers=self._headers(),
            )
            return r.status_code == 200
        except Exception:
            return False

    def verify_token(self, token: str) -> Optional[dict]:
        """Verify magic link token and get JWT."""
        try:
            r = self._client.get(f"{self.base_url}/api/auth/verify?token={token}")
            if r.status_code == 200:
                return r.json()
            return None
        except Exception:
            return None

    # Clients
    def get_clients(self) -> list:
        """Get all clients."""
        try:
            r = self._client.get(
                f"{self.base_url}/api/clients",
                headers=self._headers(),
            )
            return r.json() if r.status_code == 200 else []
        except Exception:
            return []

    # Projects
    def get_projects(self) -> list:
        """Get all projects."""
        try:
            r = self._client.get(
                f"{self.base_url}/api/projects",
                headers=self._headers(),
            )
            return r.json() if r.status_code == 200 else []
        except Exception:
            return []

    def get_project(self, project_id: str) -> Optional[dict]:
        """Get single project."""
        try:
            r = self._client.get(
                f"{self.base_url}/api/projects/{project_id}",
                headers=self._headers(),
            )
            return r.json() if r.status_code == 200 else None
        except Exception:
            return None

    # Videos
    def get_videos(self, project_id: str = None) -> list:
        """Get all videos, optionally filtered by project."""
        try:
            url = f"{self.base_url}/api/videos"
            if project_id:
                url += f"?project_id={project_id}"
            r = self._client.get(url, headers=self._headers())
            return r.json() if r.status_code == 200 else []
        except Exception:
            return []

    def approve_video(self, video_id: str) -> bool:
        """Approve a video."""
        try:
            r = self._client.post(
                f"{self.base_url}/api/videos/{video_id}/approve",
                headers=self._headers(),
            )
            return r.status_code == 200
        except Exception:
            return False

    def reject_video(self, video_id: str, reason: str = None) -> bool:
        """Reject a video with optional reason."""
        try:
            r = self._client.post(
                f"{self.base_url}/api/videos/{video_id}/reject",
                json={"reason": reason} if reason else {},
                headers=self._headers(),
            )
            return r.status_code == 200
        except Exception:
            return False

    # Pipeline
    def generate_script(self, project_id: str, data: dict) -> Optional[dict]:
        """Generate script for a video."""
        try:
            r = self._client.post(
                f"{self.base_url}/api/pipeline/script",
                json={"project_id": project_id, **data},
                headers=self._headers(),
            )
            return r.json() if r.status_code == 200 else None
        except Exception:
            return None

    def generate_images(self, video_id: str) -> Optional[list]:
        """Generate images for a video."""
        try:
            r = self._client.post(
                f"{self.base_url}/api/pipeline/images",
                json={"video_id": video_id},
                headers=self._headers(),
            )
            return r.json() if r.status_code == 200 else None
        except Exception:
            return None

    def generate_voiceover(self, video_id: str) -> Optional[dict]:
        """Generate voiceover for a video."""
        try:
            r = self._client.post(
                f"{self.base_url}/api/pipeline/voiceover",
                json={"video_id": video_id},
                headers=self._headers(),
            )
            return r.json() if r.status_code == 200 else None
        except Exception:
            return None

    # Generic async post for webhook triggers
    async def post(self, path: str, data: dict) -> dict:
        """Generic async POST request."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                r = await client.post(
                    f"{self.base_url}/api{path}",
                    json=data,
                    headers=self._headers(),
                )
                return r.json() if r.status_code in (200, 201) else {"status": "error", "message": r.text}
            except Exception as e:
                return {"status": "error", "message": str(e)}


# Global client instance
api_client = APIClient()
