import pydantic_settings

from lib.repository.redis import RedisUrl


class RedisSettings(pydantic_settings.BaseSettings):
    """Redis for redis."""

    redis_host: str
    redis_port: int

    @property
    def redis_uri(self) -> RedisUrl:
        """Return full redis url"""
        return f"redis://{self.redis_host}:{self.redis_port}/0"
