import pydantic_settings


class RedisSettings(pydantic_settings.BaseSettings):
    """Redis for redis."""

    redis_host: str
    redis_port: int
