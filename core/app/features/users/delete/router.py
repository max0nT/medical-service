import http
import typing

import fastapi

from dishka.integrations.fastapi import FromDishka, inject

from app.domain.entities.user import User
from app.features.users.delete.command import DeleteUserCommand
from app.features.users.delete.handler import DeleteUserHandler
from lib.fastapi.request import Request, get_request

router = fastapi.APIRouter(tags=["Users"])


@router.delete(
    "/users/{pk}/",
    status_code=http.HTTPStatus.NO_CONTENT,
)
@inject
async def delete_user(
    request: typing.Annotated[Request | None, fastapi.Depends(get_request)],
    handler: FromDishka[DeleteUserHandler],
    pk: int,
) -> fastapi.Response:
    """Delete `User` instance."""
    assert request is not None
    if not isinstance(request.user, User):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail={
                "detail": "Unauthorized",
            },
        )

    await handler(
        command=DeleteUserCommand(
            pk=pk,
            current_user_id=request.user.id,
        ),
        request=request,
    )
    return fastapi.Response(status_code=http.HTTPStatus.NO_CONTENT)
