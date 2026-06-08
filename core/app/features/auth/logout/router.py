import http
import typing

import fastapi
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from dishka.integrations.fastapi import FromDishka, inject

from app.features.auth.logout.command import LogoutCommand
from app.features.auth.logout.handler import LogoutHandler

router = fastapi.APIRouter(tags=["Users"])
bearer_scheme = HTTPBearer()


@router.post(
    "/users/logout/",
    status_code=http.HTTPStatus.NO_CONTENT,
)
@inject
async def logout(
    credentials: typing.Annotated[
        HTTPAuthorizationCredentials,
        fastapi.Depends(bearer_scheme),
    ],
    handler: FromDishka[LogoutHandler],
) -> fastapi.Response:
    """Do logout."""
    await handler(
        command=LogoutCommand(
            token=credentials.credentials,
        ),
    )
    return fastapi.Response(status_code=http.HTTPStatus.NO_CONTENT)
