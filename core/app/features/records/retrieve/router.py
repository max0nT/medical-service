import typing

import fastapi

from dishka.integrations.fastapi import FromDishka, inject

from app.features.records.dto import RecordReadDTO
from app.features.records.retrieve.command import RetrieveRecordCommand
from app.features.records.retrieve.handler import RetrieveRecordHandler
from lib.fastapi.request import Request, get_request

router = fastapi.APIRouter(tags=["Records"])


@router.get(
    "/records/{pk}/",
    response_model=RecordReadDTO,
)
@inject
async def retrieve_record(
    request: typing.Annotated[Request | None, fastapi.Depends(get_request)],
    handler: FromDishka[RetrieveRecordHandler],
    pk: int,
) -> RecordReadDTO:
    """Return one `Record` instance by id."""
    assert request is not None
    record = await handler(
        request=request,
        command=RetrieveRecordCommand(pk=pk),
    )
    return RecordReadDTO.model_validate(record)
