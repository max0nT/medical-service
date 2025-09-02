import typing
import datetime

from redis import asyncio as aioredis, typing as redis_typing

from config import redis_config


class RedisClient:
    """Api client for redis database."""

    def __init__(self):
        self.client: aioredis.Redis = aioredis.Redis(
            host=redis_config.redis_host,
            port=redis_config.redis_port,
        )

    async def set_value(
        self,
        key: int,
        value: typing.Any,
        exp: int | datetime.timedelta | None = None,
    ) -> None:
        """Set new value to redis store."""
        await self.client.set(
            name=key,
            value=value,
            ex=exp,
        )

    async def get_value(
        self,
        name: str,
    ) -> typing.Any:
        """Check element exist in list."""
        response: redis_typing.ResponseT = await self.client.get(
            name=name,
        )
        return response

    async def __aenter__(self) -> aioredis.Redis:
        """Return object as context handler."""
        return await self.client.__aenter__()

    async def _aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.client.__aexit__(exc_type, exc_val, exc_tb)
