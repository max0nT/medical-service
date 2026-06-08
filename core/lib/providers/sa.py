import typing

from dishka import Provider, Scope, provide
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

AsyncSessionMaker = async_sessionmaker[AsyncSession]


class SaAsyncSessionProvider(Provider):
    """Provider class for async session."""

    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def get_engine(self, uri: URL) -> AsyncEngine:
        """Provide database engine."""
        return create_async_engine(
            uri,
            future=True,
        )

    @provide(scope=Scope.APP)
    async def get_sessionmaker(
        self,
        engine: AsyncEngine,
    ) -> AsyncSessionMaker:
        """Provide `sessionmaker` class."""
        return AsyncSessionMaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def get_db_session(
        self,
        sessionmaker: AsyncSessionMaker,
    ) -> typing.AsyncGenerator[AsyncSession]:
        """Provide database session."""
        async with sessionmaker() as db_session:
            yield db_session
