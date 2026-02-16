import typing

import pydantic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.relationships import _RelationshipDeclared

T = typing.TypeVar("T")

JOINED_RELATIONS: typing.TypeAlias = typing.Sequence[
    tuple[_RelationshipDeclared[typing.Any], ...]
]


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
        *args,
        limit: int = 15,
        offset: int = 0,
        joined_relations: JOINED_RELATIONS | None = None,
        with_for_update: bool = False,
        select_one: bool = False,
        **data: typing.Any,
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
