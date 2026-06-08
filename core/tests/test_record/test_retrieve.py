import httpx

from src import models
from src.entities.record import RecordReadSchema


async def test_api(
    record: models.Record,
    authorized_api_client: httpx.AsyncClient,
) -> None:
    """Test record retrieve works correctly."""
    response: httpx.Response = await authorized_api_client.get(
        f"/records/{record.id}/",
    )
    assert response.is_success
    assert response.status_code == httpx.codes.OK
    response_data = RecordReadSchema.model_validate_json(
        response.content,
    )
    assert response_data.id == record.id
