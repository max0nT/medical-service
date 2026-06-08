from dishka import Provider, Scope, from_context, provide

from lib.repository.redis import RedisAPIClient, RedisUrl


class RedisProvider(Provider):
    """Provider class for redis connection."""

    scope = Scope.REQUEST

    redis_uri = from_context(RedisUrl, scope=Scope.APP)

    @provide(scope=Scope.REQUEST)
    def redis_client(self, uri: RedisUrl) -> RedisAPIClient:
        """Create redis api client."""
        return RedisAPIClient(uri=uri)
