import typing

import fastapi

from config import settings

from src import dependencies, extensions, models


async def authorize(
    request: fastapi.Request,
    next_call: typing.Callable,
) -> fastapi.Response:
    """Authenticate user vie bearer token."""
    user = None
    if "authorization" in request.headers:
        auth_client = dependencies.get_auth_client()

        token = await dependencies.oauth2_scheme(request=request)
        user_id = await auth_client.check_token_is_valid(
            token=token,
        )
        async with settings.session_factory() as session:
            user_repo = dependencies.get_repo(modelClass=models.User)()
            user: models.User | None = await user_repo.select_one(
                session=session,
                pk=user_id,
            )
            await session.close()

    request = extensions.Request(user=user, **request.__dict__)
    response = await next_call(request)
    return response
