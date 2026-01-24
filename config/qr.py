import pydantic_settings


class QrApiSettings(pydantic_settings.BaseSettings):
    """Config class for qr code settings."""

    qr_api_key: str
