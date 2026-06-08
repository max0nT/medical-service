import http
import typing

import fastapi

from dishka.integrations.fastapi import FromDishka, inject

from app.features.records.delete.command import DeleteRecordCommand
from app.features.records.delete.handler import DeleteRecordHandler
from lib.fastapi.request import Request, get_request

router = fastapi.APIRouter(tags=["Records"])


@router.delete(
    "/records/{pk}/",
    status_code=http.HTTPStatus.NO_CONTENT,
)
@inject
async def delete_record(
    request: typing.Annotated[Request | None, fastapi.Depends(get_request)],
    handler: FromDishka[DeleteRecordHandler],
    pk: int,
) -> fastapi.Response:
    """Delete `Record` instance."""
    assert request is not None
    await handler(
        request=request,
        command=DeleteRecordCommand(pk=pk),
    )
    return fastapi.Response(status_code=http.HTTPStatus.NO_CONTENT)
