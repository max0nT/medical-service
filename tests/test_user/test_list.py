import httpx
import sqlalchemy
import pytest
import pytest_lazy_fixtures
import pydantic

from config import database
from src import models, entities


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
    ]
)
async def test_api(
    api_client: httpx.AsyncClient,
    expected_status_code: int,
) -> None:
    """Test user lists works correctly."""

    response: httpx.Response = await api_client.get(
        "/users/"
    )

    assert response.status_code == expected_status_code

    if not response.is_success:
        return

    response_data = pydantic.TypeAdapter(list[entities.UserReadSchema]).validate_json(response.content)

    async with database.session_factory() as session:
        raw = await session.execute(
            sqlalchemy.select(models.User)
            .where(
                models.User.id.in_([entry.id for entry in response_data])
            )
        )
        entries = raw.scalars().all()

    assert len(entries) == len(response_data)
    assert (
        set([entry.id for entry in entries])
        == set([entry.id for entry in response_data])
    )
