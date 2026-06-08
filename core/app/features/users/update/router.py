import typing

import fastapi

from dishka.integrations.fastapi import FromDishka, inject

from app.domain.entities.user import User
from app.features.users.me.dto import UserReadDTO
from app.features.users.update.command import UpdateUserCommand
from app.features.users.update.dto import UserUpdateDTO
from app.features.users.update.handler import UpdateUserHandler
from lib.fastapi.request import Request, get_request

router = fastapi.APIRouter(tags=["Users"])


@router.put(
    "/users/{pk}/",
    response_model=UserReadDTO,
)
@inject
async def update_user(
    request: typing.Annotated[Request | None, fastapi.Depends(get_request)],
    handler: FromDishka[UpdateUserHandler],
    pk: int,
    data: UserUpdateDTO,
) -> UserReadDTO:
    """Update `User` instance."""
    assert request is not None
    if not isinstance(request.user, User):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail={
                "detail": "Unauthorized",
            },
        )

    user = await handler(
        command=UpdateUserCommand(
            pk=pk,
            current_user_id=request.user.id,
            first_name=data.first_name,
            last_name=data.last_name,
            sync_with_google_calendar=data.sync_with_google_calendar,
            avatar=data.avatar,
        ),
        request=request,
    )
    return UserReadDTO.model_validate(user)
