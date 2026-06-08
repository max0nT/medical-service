import http
import typing

import fastapi

from dishka.integrations.fastapi import FromDishka, inject

from app.domain.entities.user import User
from app.features.records.create.command import CreateRecordCommand
from app.features.records.create.handler import CreateRecordHandler
from app.features.records.dto import RecordReadDTO, RecordWriteDTO
from lib.fastapi.request import Request, get_request

router = fastapi.APIRouter(tags=["Records"])


@router.post(
    "/records/",
    response_model=RecordReadDTO,
    status_code=http.HTTPStatus.CREATED,
)
@inject
async def create_record(
    request: typing.Annotated[Request | None, fastapi.Depends(get_request)],
    handler: FromDishka[CreateRecordHandler],
    data: RecordWriteDTO,
) -> RecordReadDTO:
    """Create `Record` instance."""
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
        command=CreateRecordCommand(
            created_by_id=request.user.id,
            start=data.start,
            end=data.end,
        ),
    )
    return RecordReadDTO.model_validate(record)
