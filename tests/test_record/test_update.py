import arrow
import httpx

from src import models
from src.entities.record import RecordWriteSchema

from .. import utils


async def test_api(
    record: models.Record,
) -> None:
    """Test record update works correctly."""
    api_client = utils.user_api_client(user=record.created_by)
    request_data = RecordWriteSchema(
        start=arrow.utcnow().date(),
        end=arrow.utcnow().shift(hours=1).date(),
    )
    response: httpx.Response = await api_client.put(
        f"/records/{record.id}/",
        content=request_data.model_dump_json(),
    )

    assert response.status_code == httpx.codes.OK


async def test_update_by_not_employee(
    record: models.Record,
) -> None:
    """Test record update by not employee user."""
    api_client = utils.user_api_client(user=record.reserved_by)
    request_data = RecordWriteSchema(
        start=arrow.utcnow().date(),
        end=arrow.utcnow().shift(hours=1).date(),
    )
    response: httpx.Response = await api_client.put(
        f"/records/{record.id}/",
        content=request_data.model_dump_json(),
    )

    assert response.status_code == httpx.codes.FORBIDDEN
