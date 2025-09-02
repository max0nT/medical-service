import typing
from abc import ABC

import sqlalchemy

from config.database import session_factory
from src.models.core import BaseModel

ModelClass = typing.TypeVar(
    "ModelClass",
    bound=BaseModel,
)


class BaseRepository(typing.Generic[ModelClass], ABC):
    """Base repository class for interactive with database."""

    model: type[ModelClass]

    @classmethod
    async def create_repository(cls) -> typing.Self:
        return cls()

    async def get_list(
        self,
        **data: typing.Any,
    ) -> typing.Sequence[ModelClass]:
        """Return list of records from database."""
        async with session_factory() as session:
            raw_result = await session.execute(
                sqlalchemy.select(self.model).filter_by(**data),
            )
        return raw_result.scalars().all()

    async def create_one(
        self,
        **data: typing.Any,
    ) -> ModelClass:
        """Create instance."""
        instance = self.model(**data)
        async with session_factory() as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
        return instance

    async def retrieve_one(
        self,
        pk: int,
    ) -> ModelClass | None:
        """Return one instance by pk."""
        async with session_factory() as session:
            raw_result = await session.get(self.model, pk)
        return raw_result

    async def update_one(
        self,
        pk: int,
        **data: typing.Any,
    ) -> ModelClass | None:
        """Update instance by pk."""
        async with session_factory() as session:
            raw = await session.execute(
                sqlalchemy.update(self.model)
                .where(self.model.id == pk)
                .values(**data)
                .returning(self.model),
            )
            result = raw.scalar_one()
            await session.commit()
        return result

    async def delete_one(
        self,
        pk: int,
    ) -> int:
        """Delete instance."""
        async with session_factory() as session:
            result = await session.execute(
                sqlalchemy.delete(self.model).where(self.model.id == pk),
            )
        return result.rowcount
