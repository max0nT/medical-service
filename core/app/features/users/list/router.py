import typing

import fastapi

from dishka.integrations.fastapi import  FromDishka, inject

from app.domain.enums.user import Role
from app.features.users.list.command import ListUsersCommand, UserOrdering
from app.features.users.me.dto import UserReadDTO
from lib.fastapi.request import Request, get_request
from lib.protocols import HandlerProtocol

router = fastapi.APIRouter(tags=["Users"])


@router.get(
    "/users/",
    response_model=list[UserReadDTO],
)
@inject
async def list_users(
    request: typing.Annotated[Request | None, fastapi.Depends(get_request)],
    handler: FromDishka[HandlerProtocol],
    limit: typing.Annotated[
        int,
        fastapi.Query(ge=1, le=100),
    ] = 15,
    offset: typing.Annotated[
        int,
        fastapi.Query(ge=0),
    ] = 0,
    ordering: typing.Annotated[
        UserOrdering | None,
        fastapi.Query(),
    ] = None,
    role: typing.Annotated[
        Role | None,
        fastapi.Query(),
    ] = None,
) -> list[UserReadDTO]:
    """Return list of `User` instances."""
    assert request is not None
    users = typing.cast(
        typing.Sequence,
        await handler(
            request=request,
            command=ListUsersCommand(
                limit=limit,
                offset=offset,
                ordering=ordering,
                role=role,
            ),
        ),
    )
    return [UserReadDTO.model_validate(user) for user in users]
