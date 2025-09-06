import typing

import httpx
import pytest

from config import settings

from src import factories, models

from . import utils


@pytest.fixture(scope="session")
async def user() -> typing.AsyncGenerator[models.User, None]:
    """Return employee User instance."""
    user = await factories.UserFactory(
        role=models.User.Role.employee,
    )
    yield user
    async with settings.session_factory() as session:
        await session.delete(user)
        await session.commit()


@pytest.fixture(scope="session")
async def user_as_client() -> typing.AsyncGenerator[models.User, None]:
    """Return client User instance."""
    yield (
        user := await factories.UserFactory(
            role=models.User.Role.client,
        )
    )
    async with settings.session_factory() as session:
        await session.delete(user)
        await session.commit()


@pytest.fixture(scope="session")
async def record() -> typing.AsyncGenerator[models.Record, None]:
    """Return Record instance."""
    record = await factories.RecordFactory.create()
    yield await record.joined_load("*")
    async with settings.session_factory() as session:
        await session.delete(record)
        await session.commit()


@pytest.fixture(scope="session")
def client() -> httpx.AsyncClient:
    """Init http client for tests."""
    return utils.client_factory()


@pytest.fixture(scope="session")
async def authorized_api_client(
    user: models.User,
) -> httpx.AsyncClient:
    """Return authorized api client."""
    return utils.user_api_client(user=user)
