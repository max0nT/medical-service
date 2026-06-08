import typing

import fastapi

from dishka.integrations.fastapi import FromDishka, inject

from app.domain.entities.user import User
from app.features.records.dto import RecordReadDTO
from app.features.records.reserve.command import ReserveRecordCommand
from app.features.records.reserve.handler import ReserveRecordHandler
from lib.fastapi.request import Request, get_request

router = fastapi.APIRouter(tags=["Records"])


@router.put(
    "/records/reserve/{pk}/",
    response_model=RecordReadDTO,
)
@inject
async def reserve_record(
    request: typing.Annotated[Request | None, fastapi.Depends(get_request)],
    handler: FromDishka[ReserveRecordHandler],
    pk: int,
) -> RecordReadDTO:
    """Reserve `Record` instance."""
    assert request is not None
    if not isinstance(request.user, User):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail={
                "detail": "Unauthorized",
            },
        )

    record = await handler(
        request=request,
        command=ReserveRecordCommand(
            pk=pk,
            user_id=request.user.id,
            user_email=request.user.email,
        ),
    )
    return RecordReadDTO.model_validate(record)
