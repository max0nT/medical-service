import typing

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.core import BaseModel

T = typing.TypeVar(
    "T",
    bound=BaseModel,
)

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
        **data: typing.Any,
    ) -> typing.Sequence[T]:
        """Return list of records from database."""
        raw_result = await session.execute(
            sqlalchemy.select(self.model).where(*args).filter_by(**data),
        )
        return raw_result.scalars().all()

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

    async def select_one(
        self,
        session: AsyncSession,
        pk: int,
        raise_error: bool = False,
    ) -> T | None:
        """Return one instance by pk."""
        return await session.get(self.model, pk)

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
