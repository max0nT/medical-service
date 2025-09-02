import pydantic_settings


class RedisSettings(pydantic_settings.BaseSettings):
    """Redis for redis."""

    model_config = pydantic_settings.SettingsConfigDict(
        env_file="config/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    redis_host: str
    redis_port: int


redis_config = RedisSettings()
