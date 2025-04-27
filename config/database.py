import typing

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

database_url = URL.create(
    "postgresql+asyncpg",
    username="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5435,
    database="postgres",
)
engine = create_async_engine(database_url.render_as_string())
session_factory = async_sessionmaker(engine)


async def session() -> typing.AsyncGenerator:
    """Generate connect session for making queries."""
    async with session_factory() as session:
        yield session


Base = declarative_base()
