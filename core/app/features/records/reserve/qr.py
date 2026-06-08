import base64

import fastapi

import aiohttp

from app.infrastructure.config import settings


class QRCodeClient:
    """Client which interacts with qr code generator API."""

    base_url = "https://www.qrcoder.co.uk/api/v4/"

    async def get_qr_code(self, profile_url: str) -> bytes:
        """Return qr code image bytes."""
        async with aiohttp.ClientSession(self.base_url) as session:
            async with session.get(
                "",
                params=self.get_params(profile_url),
            ) as response:
                response.raise_for_status()
                return await response.content.read()

    def get_params(self, profile_url: str) -> dict[str, str]:
        """Return QR API query params."""
        return {
            "key": settings.qr_api_key,
            "text": profile_url,
        }


class QrCodeGenerator:
    """Class to generate qr code for user profile."""

    def __init__(
        self,
        qr_code_client: QRCodeClient,
    ) -> None:
        self.qr_code_client = qr_code_client

    async def generate(self, user_id: int) -> str:
        """Return qr code in base64 format."""
        content = await self.qr_code_client.get_qr_code(
            profile_url=self.generate_user_profile(user_id=user_id),
        )
        return base64.b64encode(content).decode()

    def generate_user_profile(self, user_id: int) -> str:
        """Return user profile url."""
        return (
            f"http://test/users/{user_id}/"
        )
