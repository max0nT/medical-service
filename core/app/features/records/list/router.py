import typing

import fastapi

from dishka.integrations.fastapi import FromDishka, inject

from app.features.records.dto import RecordReadDTO
from app.features.records.list.command import ListRecordsCommand
from lib.fastapi.request import Request, get_request
from lib.protocols import HandlerProtocol

router = fastapi.APIRouter(tags=["Records"])


@router.get(
    "/records/",
    response_model=list[RecordReadDTO],
)
@inject
async def list_records(
    request: typing.Annotated[Request | None, fastapi.Depends(get_request)],
    handler: FromDishka[HandlerProtocol],
    created_by: int | None = None,
    reserved_by: int | None = None,
) -> list[RecordReadDTO]:
    """Return list of `Record` instances."""
    assert request is not None
    records = typing.cast(
        typing.Sequence,
        await handler(
            request=request,
            command=ListRecordsCommand(
                created_by=created_by,
                reserved_by=reserved_by,
            ),
        ),
    )
    return [RecordReadDTO.model_validate(record) for record in records]
