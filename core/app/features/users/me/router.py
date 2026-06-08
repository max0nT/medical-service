import typing

import fastapi

from app.domain.entities.user import User
from app.features.users.me.dto import UserReadDTO
from lib.fastapi.request import Request, get_request

router = fastapi.APIRouter(tags=["Users"])


@router.get(
    "/users/me/",
    response_model=UserReadDTO,
)
async def me(
    request: typing.Annotated[Request | None, fastapi.Depends(get_request)],
) -> UserReadDTO:
    """Get info about user by access token."""
    assert request is not None
    if not isinstance(request.user, User):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail={
                "detail": "Unauthorized",
            },
        )

    return UserReadDTO.model_validate(request.user)
