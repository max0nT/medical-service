import typing

import pytest
import httpx

from config import database
from src.app import app
from src import models, factories, services, entities


def client_factory() -> httpx.AsyncClient:
    """Generate api client."""
    return httpx.AsyncClient(
        transport=httpx.ASGITransport(
            app=app,
        ),
        base_url="http://api",
    )


@pytest.fixture(scope="session")
async def user() -> typing.AsyncGenerator[models.User, None]:
    """Return User instance."""
    user = await factories.UserFactory()
    yield user
    async with database.session_factory() as session:
        await session.delete(user)
        await session.commit()


@pytest.fixture(scope="session")
def client() -> httpx.AsyncClient:
    """Init http client for tests."""
    return client_factory()


@pytest.fixture(scope="session")
async def authorized_api_client(
    user: models.User,
) -> httpx.AsyncClient:
    """Return authorized api client."""
    authorizer = services.AuthClient.create_auth_client()
    token = await authorizer.authenticate(
        entities.UserSignInSchema(
            email=user.email,
            password=factories.USER_PASSWORD,
        ),
    )
    api_client = client_factory()
    api_client.headers["authorization"] = f"Bearer {token}"
    return api_client
