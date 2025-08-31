import json

import httpx

from src import models, factories, entities


async def test_sign_in(
    user: models.User,
    client: httpx.AsyncClient,
) -> None:
    """Test sign in works correctly."""
    request_data = entities.UserSignInSchema(
        email=user.email,
        password=factories.USER_PASSWORD,
    )

    response: httpx.Response = await client.post(
        url="/users/login/",
        content=request_data.model_dump_json(),
    )

    assert response.is_success
    assert response.status_code == httpx.codes.OK

    response_data: entities.AuthToken = entities.AuthToken.model_validate_json(
        response.content,
    )
    assert response_data


async def test_sign_in_with_wrong_data(
    user: models.User,
    client: httpx.AsyncClient,
) -> None:
    """Test sign in with wrong data."""
    request_data = entities.UserSignInSchema(
        email=user.email,
        password="wrong_password",
    )

    response: httpx.Response = await client.post(
        url="/users/login/",
        content=request_data.model_dump_json(),
    )

    assert response.is_client_error
    assert response.status_code == httpx.codes.BAD_REQUEST

    response_data = json.loads(response.content)
    assert response_data["detail"]["detail"] == "Wrong email or password."
