import httpx
import pydantic
import pytest
import pytest_lazy_fixtures

from config import settings

from src import dependencies, entities, models


@pytest.mark.parametrize(
    argnames=[
        "api_client",
        "expected_status_code",
    ],
    argvalues=[
        [
            pytest_lazy_fixtures.lf("client"),
            httpx.codes.UNAUTHORIZED,
        ],
        [
            pytest_lazy_fixtures.lf("authorized_api_client"),
            httpx.codes.OK,
        ],
    ],
)
async def test_api(
    api_client: httpx.AsyncClient,
    expected_status_code: int,
    record: models.Record,
) -> None:
    """Test record lists works correctly."""

    response: httpx.Response = await api_client.get("/records/")

    assert response.status_code == expected_status_code

    if not response.is_success:
        return

    response_data = pydantic.TypeAdapter(
        list[entities.RecordReadSchema],
    ).validate_json(response.content)
    response_ids = [record_data.id for record_data in response_data]

    repo = dependencies.get_repo(modelClass=models.Record)()
    session = settings.session_factory()
    record_list = await repo.select(
        session,
        models.Record.id.in_(response_ids),
    )
    await session.close()
    ids = {entity.id for entity in record_list}
    assert ids
    assert set(ids) == set(response_ids)
