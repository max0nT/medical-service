import typing
from abc import ABC

import sqlalchemy
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing_extensions import AsyncGenerator

import config as settings
from src.models.core import BaseModel

ModelClass = typing.TypeVar(
    "ModelClass",
    bound=BaseModel,
)


class BaseRepository(typing.Generic[ModelClass], ABC):
    """Base repository class for interactive with database."""

    model: type[ModelClass]

    def __init__(
        self,
        session: AsyncSession,
        generator: AsyncGenerator[AsyncSession, None],
    ):
        self.session = session
        self.generator = generator

    @classmethod
    async def create_repository(cls) -> typing.Self:
        generator = settings.session_generator()
        session = await generator.asend(None)
        return cls(session=session, generator=generator)

    async def get_list(self, **data: typing.Any) -> typing.Sequence[ModelClass]:
        """Return list of records from database."""
        raw_result = await self.session.execute(
            sqlalchemy.select(self.model).filter_by(**data),
        )
        await self._close_session()
        return raw_result.scalars().all()

    async def create_one(
        self,
        **data: typing.Any,
    ) -> ModelClass:
        """Create isntance."""
        raw_result = await self.session.execute(
            sqlalchemy.insert(self.model).values(**data),
        )
        await self._close_session()
        return raw_result.scalar_one()

    async def retrieve_one(
        self,
        pk: int,
    ) -> ModelClass | None:
        """Retrun one instance by pk."""
        raw_result = await self.session.get(self.model, pk)
        await self._close_session()
        return raw_result

    async def update_one(
        self,
        pk: int,
        **data: typing.Any,
    ) -> ModelClass | None:
        """Update instance."""
        raw_result = await self.session.execute(
            sqlalchemy.update(self.model).where(self.model.id == pk).values(**data),
        )
        await self._close_session()
        return raw_result.scalar_one_or_none()

    async def delete_one(
        self,
        pk: int,
    ) -> int:
        """Delete instance."""
        raw_result = await self.session.execute(
            sqlalchemy.delete(self.model).where(self.model.id == pk)
        )
        await self._close_session()
        return raw_result.rowcount

    async def reconnect(self) -> None:
        """Setup db session again."""
        self.generator = settings.session_generator()
        self.session = await self.generator.asend(None)

    async def _close_session(self) -> None:
        """Close db session."""
        await self.generator.aclose()
