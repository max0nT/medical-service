import typing

from config import database

import pytest

from sqlalchemy.ext import asyncio as asyncio_ext


@pytest.fixture(scope="session")
def engine() -> asyncio_ext.AsyncEngine:
    """Init engine for testing."""
    return asyncio_ext.create_async_engine(database.database_url)


@pytest.fixture(scope="session")
async def session_factory(
    engine: asyncio_ext.AsyncEngine,
) -> typing.AsyncGenerator[asyncio_ext.async_sessionmaker, None]:
    """Init schema in testing database."""
    async with engine.begin() as connection:
        yield asyncio_ext.async_sessionmaker(bind=connection)
        await connection.rollback()


@pytest.fixture(scope="session")
async def session(
    session_factory: asyncio_ext.async_sessionmaker,
) -> typing.AsyncGenerator[asyncio_ext.AsyncSession, None]:
    """Init global session for testing."""
    session: asyncio_ext.AsyncSession = session_factory()
    yield session
    await session.close()
