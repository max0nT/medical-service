import typing

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.relationships import _RelationshipDeclared

from lib.exceptions import ObjectNotFoundException, UnsolvableAnnotationsError
from lib.model.base import BaseModel
from lib.types import infer_type_args

T = typing.TypeVar("T", bound=BaseModel)

JOINED_RELATIONS: typing.TypeAlias = typing.Sequence[
    tuple[_RelationshipDeclared[typing.Any], ...]
]


class BaseRepository(typing.Generic[T]):
    """Base repository class for interactive with database."""

    model_base: type[BaseModel]

    def __init_subclass__(cls):
        """Get model class from type hints."""
        type_hints = infer_type_args(cls, BaseRepository)
        if len(type_hints) != 1:
            raise UnsolvableAnnotationsError(
                f"Repository class must have only one type hint, but got "
                f" {type_hints}",
            )
        cls.model_base = type_hints[0]
        return super().__init_subclass__()

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def select(
        self,
        *args,
        limit: int = 15,
        offset: int = 0,
        joined_relations: JOINED_RELATIONS | None = None,
        with_for_update: bool = False,
        select_one: bool = False,
        stmt: sqlalchemy.Select | None = None,
        **data: typing.Any,
    ) -> typing.Sequence[T]:
        """Return list of records from database."""
        raw_result = await self.session.execute(
            statement=self._get_select_query(
                *args,
                limit=limit,
                offset=offset,
                with_for_update=with_for_update,
                joined_relations=joined_relations,
                stmt=stmt,
                **data,
            ),
        )

        if select_one:
            return raw_result.scalar_one_or_none()
        return raw_result.scalars().fetchall()

    async def select_one(
        self,
        pk: int,
    ) -> T | None:
        """Return one instance by pk."""
        instance = await self.session.get(self.model_base, pk)
        if instance is None:
            raise ObjectNotFoundException(
                f"{self.model_base.__name__} with {pk=} not found.",
            )
        return instance

    async def count(
        self,
        session: AsyncSession,
        *args,
        limit: int = 15,
        offset: int = 0,
        **data: typing.Any,
    ) -> int:
        """Get count of selected rows."""
        raw = await session.execute(
            self._get_select_query(*args, limit=limit, offset=offset, **data),
        )
        return raw.count()

    async def add(
        self,
        instance: T,
        flush: bool = False,
    ) -> None:
        """Create instance."""
        self.session.add(instance)
        if flush:
            await self.session.flush(instance)
            await self.session.refresh(instance)

    async def delete(
        self,
        instance: T,
    ) -> None:
        """Delete instance."""
        await self.session.delete(instance)

    def _get_select_query(
        self,
        *args,
        limit: int = 15,
        offset: int = 15,
        with_for_update: bool = False,
        joined_relations: JOINED_RELATIONS | None,
        stmt: sqlalchemy.Select | None = None,
        **data: typing.Any,
    ) -> sqlalchemy.Select:
        """Get select query."""
        if stmt is not None:
            return stmt
        select_query = (
            sqlalchemy.select(self.model)
            .where(*args)
            .filter_by(**data)
            .limit(limit)
            .offset(offset)
        )
        if joined_relations:
            select_query = self._set_relationship_load_options(
                query=select_query,
                relations=joined_relations,
            )
        if with_for_update:
            select_query = select_query.with_for_update()
        return select_query

    def _set_relationship_load_options(
        self,
        query: sqlalchemy.Select,
        relations: JOINED_RELATIONS,
    ) -> sqlalchemy.Select:
        """Return select with joined load options."""
        options = []
        for relation in relations:
            options.append(joinedload(*relation))
        return query.options(*options)
