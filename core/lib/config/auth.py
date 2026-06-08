import pydantic_settings


class AuthSettings(pydantic_settings.BaseSettings):
    """Settings class for auth."""

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
