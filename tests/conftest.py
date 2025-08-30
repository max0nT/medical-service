import typing

import pytest
import httpx
from sqlalchemy.ext import asyncio as asyncio_ext

from config import database
from src.app import app
from src import models, factories


@pytest.fixture(scope="session")
async def session_factory() -> typing.AsyncGenerator[
    asyncio_ext.async_sessionmaker,
    None,
]:
    """Init test transaction."""
    async with database.engine.begin() as connection:
        yield
        await connection.rollback()


@pytest.fixture(scope="session")
def client() -> httpx.AsyncClient:
    """Init http client for tests."""
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
