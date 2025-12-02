"""Google Drive service for video delivery."""

import json
import logging
from pathlib import Path
from typing import Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config import get_settings

logger = logging.getLogger(__name__)

# Scopes needed for Drive access
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


class GoogleDriveService:
    """Service for uploading videos to Google Drive."""

    def __init__(self):
        self.settings = get_settings()
        self._service = None
        self._credentials = None

    def _get_credentials(self):
        """Load service account credentials."""
        if self._credentials:
            return self._credentials

        # Try loading from JSON file first (for local dev)
        creds_path = Path("google-credentials.json")
        if creds_path.exists():
            self._credentials = service_account.Credentials.from_service_account_file(
                str(creds_path), scopes=SCOPES
            )
            return self._credentials

        # Try loading from environment variable (for production)
        creds_json = self.settings.google_service_account_json
        if creds_json:
            creds_info = json.loads(creds_json)
            self._credentials = service_account.Credentials.from_service_account_info(
                creds_info, scopes=SCOPES
            )
            return self._credentials

        raise ValueError(
            "Google credentials not found. Provide google-credentials.json file "
            "or set GOOGLE_SERVICE_ACCOUNT_JSON environment variable."
        )

    def _get_service(self):
        """Get or create Drive service."""
        if self._service:
            return self._service

        credentials = self._get_credentials()
        self._service = build("drive", "v3", credentials=credentials)
        return self._service

    def create_client_folder(self, client_name: str) -> str:
        """Create a folder for a client in Google Drive.

        Args:
            client_name: Name of the client

        Returns:
            Folder ID of the created folder
        """
        service = self._get_service()

        # Check if folder already exists
        parent_folder = self.settings.google_drive_folder_id
        query = f"name='{client_name}' and mimeType='application/vnd.google-apps.folder'"
        if parent_folder:
            query += f" and '{parent_folder}' in parents"

        results = service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get("files", [])

        if files:
            logger.info(f"Folder '{client_name}' already exists: {files[0]['id']}")
            return files[0]["id"]

        # Create new folder
        folder_metadata = {
            "name": client_name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_folder:
            folder_metadata["parents"] = [parent_folder]

        folder = service.files().create(body=folder_metadata, fields="id").execute()
        folder_id = folder.get("id")
        logger.info(f"Created folder '{client_name}': {folder_id}")
        return folder_id

    def upload_video(
        self,
        file_path: str,
        filename: str,
        folder_id: Optional[str] = None,
        description: Optional[str] = None,
    ) -> dict:
        """Upload a video file to Google Drive.

        Args:
            file_path: Local path to the video file
            filename: Name to give the file in Drive
            folder_id: Optional folder ID to upload to
            description: Optional description for the file

        Returns:
            Dict with file ID and web view link
        """
        service = self._get_service()

        file_metadata = {"name": filename}
        if description:
            file_metadata["description"] = description
        if folder_id:
            file_metadata["parents"] = [folder_id]
        elif self.settings.google_drive_folder_id:
            file_metadata["parents"] = [self.settings.google_drive_folder_id]

        # Determine mime type
        path = Path(file_path)
        mime_types = {
            ".mp4": "video/mp4",
            ".mov": "video/quicktime",
            ".avi": "video/x-msvideo",
            ".webm": "video/webm",
        }
        mime_type = mime_types.get(path.suffix.lower(), "video/mp4")

        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id,webViewLink,webContentLink")
            .execute()
        )

        logger.info(f"Uploaded '{filename}' to Google Drive: {file.get('id')}")
        return {
            "file_id": file.get("id"),
            "web_view_link": file.get("webViewLink"),
            "download_link": file.get("webContentLink"),
        }

    def set_file_permissions(
        self, file_id: str, email: Optional[str] = None, anyone_with_link: bool = False
    ) -> None:
        """Set permissions on a file.

        Args:
            file_id: ID of the file
            email: Email to share with (reader access)
            anyone_with_link: If True, anyone with the link can view
        """
        service = self._get_service()

        if anyone_with_link:
            permission = {"type": "anyone", "role": "reader"}
            service.permissions().create(fileId=file_id, body=permission).execute()
            logger.info(f"Set anyone-with-link permission on {file_id}")

        if email:
            permission = {"type": "user", "role": "reader", "emailAddress": email}
            service.permissions().create(
                fileId=file_id, body=permission, sendNotificationEmail=False
            ).execute()
            logger.info(f"Shared {file_id} with {email}")

    def get_file_link(self, file_id: str) -> str:
        """Get the web view link for a file.

        Args:
            file_id: ID of the file

        Returns:
            Web view link
        """
        service = self._get_service()
        file = service.files().get(fileId=file_id, fields="webViewLink").execute()
        return file.get("webViewLink")


# Singleton instance
drive_service = GoogleDriveService()
