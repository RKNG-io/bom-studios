"""Email service using Resend."""

import logging

import resend

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def send_magic_link_email(to_email: str, token: str) -> bool:
    """
    Send a magic link email to the user.

    Returns True if sent successfully, False otherwise.
    """
    if not settings.resend_api_key:
        logger.warning("RESEND_API_KEY not configured, skipping email send")
        return False

    resend.api_key = settings.resend_api_key

    magic_link_url = f"{settings.portal_url}/login?token={token}"

    try:
        resend.Emails.send(
            {
                "from": settings.resend_from_email,
                "to": [to_email],
                "subject": "Your BOM Studios Login Link",
                "html": f"""
                <div style="font-family: Inter, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h1 style="color: #0C0C0C; font-size: 24px;">Welcome to BOM Studios</h1>
                    <p style="color: #2E2E2E; font-size: 16px; line-height: 1.5;">
                        Click the button below to sign in to your account.
                        This link will expire in {settings.magic_link_expire_minutes} minutes.
                    </p>
                    <a href="{magic_link_url}"
                       style="display: inline-block; background-color: #0C0C0C; color: #FAF9F7;
                              padding: 12px 24px; text-decoration: none; border-radius: 4px;
                              font-weight: 500; margin: 16px 0;">
                        Sign In
                    </a>
                    <p style="color: #5A5A5A; font-size: 14px; margin-top: 24px;">
                        If you didn't request this link, you can safely ignore this email.
                    </p>
                    <hr style="border: none; border-top: 1px solid #E8E6E3; margin: 24px 0;" />
                    <p style="color: #5A5A5A; font-size: 12px;">
                        BOM Studios - Video Production Platform
                    </p>
                </div>
                """,
            }
        )
        logger.info(f"Magic link email sent to {to_email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send magic link email to {to_email}: {e}")
        return False
