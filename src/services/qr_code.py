import base64

import aiohttp
import requests

from config import settings

from src import lib


class QRCodeClient:
    """Class which interacts with qr code generator API.

    Qr code is used for fast client profile check.

    """

    BASE_URL = "https://www.qrcoder.co.uk/api/v4/"

    async def get_qr_code(self, profile_url: str) -> requests.Response:
        async with aiohttp.ClientSession(self.BASE_URL) as session:
            async with session.get(
                "",
                params=self.get_params(profile_url),
            ) as response:
                return response

    def get_params(self, profile_url: str) -> dict[str, str]:
        """Get params for api url request."""
        return {
            "key": settings.qr_api_key,
            "text": profile_url,
        }


def get_qr_code_generator_client() -> QRCodeClient:
    """Generate qr code client."""
    return QRCodeClient()


class QrCodeGenerator:
    """Class to generator qr code for user profile."""

    def __init__(
        self,
        qr_code_client: QRCodeClient,
        request: lib.Request,
    ) -> None:
        self.qr_code_client = qr_code_client
        self.request = request

    async def generate(self) -> bytes:
        """Return qr code in base64 format"""
        response = await self.qr_code_client.get_qr_code(
            self.generate_user_profile(),
        )
        response.raise_for_status()
        return base64.b64encode(response.content)

    def generate_user_profile(self) -> str:
        return (
            f"{self.request.url.scheme}://{self.request.url.hostname}"
            f"/users/{self.request.user.id}/"
        )
