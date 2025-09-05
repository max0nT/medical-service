import httpx

from src import entities, factories, models
from src.redis.client import RedisAPIClient


async def test_logout(
    user: models.User,
    client: httpx.AsyncClient,
) -> None:
    """Test logout works correctly."""
    request_data = entities.UserSignInSchema(
        email=user.email,
        password=factories.USER_PASSWORD,
    )

    # Get access token
    response: httpx.Response = await client.post(
        url="/users/login/",
        content=request_data.model_dump_json(),
    )

    assert response.is_success
    assert response.status_code == httpx.codes.OK

    response_data: entities.AuthToken = entities.AuthToken.model_validate_json(
        response.content,
    )
    token = response_data.access_token
    client.headers["authorization"] = f"Bearer {token}"

    # Do logout to move token to blacklist
    logout_response: httpx.Response = await client.post(url="/users/logout/")
    assert logout_response.is_success
    assert logout_response.status_code == httpx.codes.NO_CONTENT

    # Ensure the token is in black list
    async with RedisAPIClient() as redis_client:
        response = await redis_client.get_value(name=token)

    assert response

    # Ensure API doesn't allow to make request with banned token
    profile_response = httpx.Response = await client.get(url="/users/me/")

    assert profile_response.is_client_error
    assert profile_response.status_code == httpx.codes.UNAUTHORIZED

    # Post test
    async with RedisAPIClient() as redis_client:
        await redis_client.delete_value(name=token)

    client.headers.pop("authorization")
