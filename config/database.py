import typing

from sqlalchemy.pool import NullPool
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, decl_api

database_url = URL.create(
    "postgresql+asyncpg",
    username="postgres",
    password="postgres",
    host="0.0.0.0",
    port=5435,
    database="postgres",
)
engine = create_async_engine(database_url, poolclass=NullPool)
session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def session_generator() -> typing.AsyncGenerator[AsyncSession, None]:
    """Generate connect session for making queries."""
    async with session_factory() as session:
        yield session


Base: decl_api.DeclarativeBase = declarative_base()
