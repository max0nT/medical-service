import typing

import pydantic
from sqlalchemy.ext.asyncio import AsyncSession

T = typing.TypeVar("T")

class RepositoryProtocol(typing.Protocol, typing.Generic[T]):

    async def select_one(
        self,
        session: AsyncSession,
        pk: int,
    ) -> T:
        """Select one instance by pk."""

    async def select(
        self,
        session: AsyncSession,
        pk: int,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> typing.Iterable[T]:
        """Select instance list."""

    async def insert(
        self,
        session: AsyncSession,
        **kwargs: typing.Any,
    ) -> T:
        """Insert instance."""

    async def update(
        self,
        session: AsyncSession,
        data: pydantic.BaseModel,
    ) -> T | None:
        """Update instance."""

    async def delete(
        self,
        session: AsyncSession,
        pk: int,
    ) -> int | None:
        """Delete instance."""
