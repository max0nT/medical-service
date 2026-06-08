import typing

import fastapi

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.domain.entities.user import User
from app.infrastructure.config import settings
from lib.fastapi.request import Request
from lib.jwt import JWTService
from lib.repository.redis import RedisAPIClient

engine = create_async_engine(settings.database_url, future=True)
session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def authorize(
    request: fastapi.Request,
    next_call: typing.Callable,
) -> fastapi.Response:
    """Authenticate user vie bearer token."""
    user = None
    if "authorization" in request.headers:
        auth_client = JWTService(
            settings=settings,
            redis=RedisAPIClient(uri=settings.redis_uri),
        )
        token = request.headers["authorization"].removeprefix("Bearer ")
        user_id = await auth_client.check_token_is_valid(
            token=token,
        )
        if user_id is not None:
            async with session_factory() as session:
                user = await session.get(User, user_id)

    request = Request(user=user, **request.__dict__)
    response = await next_call(request)
    return response
