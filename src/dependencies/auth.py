import http
import typing

import fastapi
from fastapi.security import OAuth2PasswordBearer

from src import models, repositories, services

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def auth_user(
    token: typing.Annotated[str, fastapi.Depends(oauth2_scheme)],
) -> models.User:
    """Get user from JWT token."""
    auth_client = services.AuthClient.create_auth_client()
    user_id = await auth_client.check_token_is_valid(token=token)
    user_repository = await repositories.UserRepository.create_repository()
    user = await user_repository.retrieve_one(pk=user_id)
    if not user:
        raise fastapi.HTTPException(
            status_code=http.HTTPStatus.UNAUTHORIZED,
            detail={
                "detail": "User not found",
            },
        )
    return user
