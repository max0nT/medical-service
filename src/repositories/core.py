import typing

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.relationships import _RelationshipDeclared

from src.models.core import BaseModel

T = typing.TypeVar(
    "T",
    bound=BaseModel,
)

JOINED_RELATIONS: typing.TypeAlias = typing.Sequence[
    tuple[_RelationshipDeclared[typing.Any], ...]
]

REPO_CLASSES = {}


class BaseRepository(typing.Generic[T]):
    """Base repository class for interactive with database."""

    def __init_subclass__(cls):
        modelClass: T = typing.get_args(cls)
        REPO_CLASSES[modelClass] = cls
        return super().__init_subclass__()

    def __init__(self, model: BaseModel) -> None:
        self.model = model

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
    ) -> typing.Sequence[T]:
        """Return list of records from database."""
        raw_result = await session.execute(
            statement=self._get_select_query(
                *args,
                limit=limit,
                offset=offset,
                with_for_update=with_for_update,
                joined_relations=joined_relations,
                **data,
            ),
        )

        if select_one:
            return raw_result.scalar_one_or_none()
        return raw_result.scalars().fetchall()

    async def select_one(
        self,
        session: AsyncSession,
        pk: int,
    ) -> T | None:
        """Return one instance by pk."""
        return await self.select(
            session=session,
            id=pk,
            select_one=True,
        )

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

    async def insert(
        self,
        session: AsyncSession,
        **data: typing.Any,
    ) -> T:
        """Create instance."""
        instance = self.model(**data)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    async def update(
        self,
        session: AsyncSession,
        pk: int,
        **data: typing.Any,
    ) -> T | None:
        """Update instance by pk."""
        raw = await session.execute(
            sqlalchemy.update(self.model)
            .where(self.model.id == pk)
            .values(**data)
            .returning(self.model),
        )
        return raw.scalar_one()

    async def delete(
        self,
        session: AsyncSession,
        pk: int,
    ) -> int:
        """Delete instance."""
        result = await session.execute(
            sqlalchemy.delete(self.model).where(self.model.id == pk),
        )
        return result.rowcount

    def _get_select_query(
        self,
        *args,
        limit: int = 15,
        offset: int = 15,
        with_for_update: bool = False,
        joined_relations: JOINED_RELATIONS | None,
        **data: typing.Any,
    ) -> sqlalchemy.Select:
        """Get select query."""
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
