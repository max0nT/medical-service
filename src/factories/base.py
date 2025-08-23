import factory
from sqlalchemy.ext import asyncio as asyncio_ext
from sqlalchemy.orm import decl_api

class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Base Factory class for testing.

    It allows to generate data in async mode.

    """

    @classmethod
    async def _create(
        cls,
        model_class: type[decl_api.DeclarativeBase],
        *args,
        session: asyncio_ext.AsyncSession,
        **kwargs,
    ) -> decl_api.DeclarativeBase:
        instance: decl_api.DeclarativeBase = model_class(*args, **kwargs)
        async with session as session:
            session.add(instance)
            await session.flush()
            await session.refresh(instance)
        return instance

    @classmethod
    async def create_batch(
        cls,
        size: int,
        session: asyncio_ext.AsyncSession,
        **kwargs,
    ):
        return [
            await cls(session=session, **kwargs)
            for _ in range(size)
        ]
