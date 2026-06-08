import fastapi

from dishka.integrations.fastapi import FromDishka, inject

from app.features.auth.login.command import LoginCommand
from app.features.auth.login.dto import AccessToken, LoginDTO
from app.features.auth.login.handler import LoginHandler

router = fastapi.APIRouter(tags=["Users"])


@router.post(
    "/users/login/",
)
@inject
async def sign_up(
    handler: FromDishka[LoginHandler],
    data: LoginDTO,
) -> AccessToken:
    """Sign up for clients."""
    token = await handler(
        command=LoginCommand(
            email=data.email,
            password=data.password,
        ),
    )
    return AccessToken(access_token=token)
