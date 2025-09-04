import httpx
import pytest
import pytest_lazy_fixtures

from src import entities, models


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
    user: models.User,
) -> None:
    """Test user retrieve works correctly."""

    response: httpx.Response = await api_client.get(f"/users/{user.id}/")

    assert response.status_code == expected_status_code

    if not response.is_success:
        return

    response_data = entities.UserReadSchema.model_validate_json(
        response.content,
    )

    assert response_data.id == user.id
