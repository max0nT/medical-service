import typing

import fastapi

from dishka.integrations.fastapi import FromDishka, inject

from app.features.records.dto import RecordReadDTO, RecordWriteDTO
from app.features.records.update.command import UpdateRecordCommand
from app.features.records.update.handler import UpdateRecordHandler
from lib.fastapi.request import Request, get_request

router = fastapi.APIRouter(tags=["Records"])


@router.put(
    "/records/{pk}/",
    response_model=RecordReadDTO,
)
@inject
async def update_record(
    request: typing.Annotated[Request | None, fastapi.Depends(get_request)],
    handler: FromDishka[UpdateRecordHandler],
    pk: int,
    data: RecordWriteDTO,
) -> RecordReadDTO:
    """Update `Record` instance."""
    assert request is not None
    record = await handler(
        request=request,
        command=UpdateRecordCommand(
            pk=pk,
            start=data.start,
            end=data.end,
        ),
    )
    return RecordReadDTO.model_validate(record)
