import httpx

from src import entities, models


async def test_api(
    authorized_api_client: httpx.AsyncClient,
    user: models.User,
) -> None:
    """Test user getting info is successfully."""

    response: httpx.Response = await authorized_api_client.get(
        url="/users/me/",
    )

    assert response.is_success
    assert response.status_code == httpx.codes.OK

    response_data = entities.UserReadSchema.model_validate_json(
        response.content,
    )
    assert response_data.id == user.id
