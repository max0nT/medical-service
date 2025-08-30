import uuid
import json

import httpx

from config import database
from src import entities, models


async def test_sign_up(
    client: httpx.AsyncClient,
):
    """Test sign up works successfully."""

    request_data = entities.UserSignUpSchema(
        email=str(uuid.uuid4()) + "@gmail.com",
        password="new_password",
        password_repeat="new_password"
    )
    response: httpx.Response = await client.post(
        url="/users/sign-up/",
        content=request_data.model_dump_json(),
    )

    assert response.is_success
    assert response.status_code == httpx.codes.CREATED

    response_data = json.loads(response.content)
    async with database.session_factory() as session:
        instance = await session.get(models.User, response_data["id"])

        assert instance and isinstance(instance, models.User)
        # Post test running
        session.delete(instance)
        await session.commit()


async def test_sign_up_with_other_password(client: httpx.AsyncClient) -> None:
    """Test sign up with not matching password."""

    request_data = entities.UserSignUpSchema(
        email=str(uuid.uuid4()) + "@gmail.com",
        password="new_password",
        password_repeat="other_password"
    )
    response: httpx.Response = await client.post(
        url="/users/sign-up/",
        content=request_data.model_dump_json(),
    )


    assert response.is_client_error
    assert response.status_code == httpx.codes.BAD_REQUEST

    response_data = json.loads(response.content)

    assert (
        response_data["detail"]["detail"]
        == "Passwords don't match"
    )


async def test_sign_up_with_existing_email(
    client: httpx.AsyncClient,
    user: models.User,
) -> None:
    """Test sign up with existing email."""
    request_data = entities.UserSignUpSchema(
        email=user.email,
        password="New_password",
        password_repeat="New_password",
    )
    response: httpx.Response = await client.post(
        url="/users/sign-up/",
        content=request_data.model_dump_json(),
        follow_redirects=True,
    )

    assert response.is_client_error
    assert response.status_code == httpx.codes.BAD_REQUEST

    response_data = json.loads(response.content)
    assert (
        response_data["detail"]["detail"]
        == f"User with email {user.email} already exists"
    )
