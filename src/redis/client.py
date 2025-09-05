import datetime
import typing

from redis import asyncio as aioredis
from redis import typing as redis_typing

from config import settings


class RedisAPIClient:
    """Api client for redis database."""

    def __init__(self):
        self.client: aioredis.Redis = aioredis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
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

    async def delete_value(
        self,
        name: str,
    ) -> typing.Any:
        """Delete element."""
        await self.client.delete(name)

    async def __aenter__(self):
        """Return object as context handler."""
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.client.__aexit__(exc_type, exc_val, exc_tb)
