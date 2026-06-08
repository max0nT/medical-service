from redis import asyncio as aioredis

type RedisUrl = str


class RedisAPIClient:
    """Api client for redis database."""

    def __init__(self, uri: RedisUrl):
        self.client: aioredis.Redis = aioredis.Redis.from_url(uri)
