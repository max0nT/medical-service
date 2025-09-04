import factory
from sqlalchemy.ext import asyncio as asyncio_ext
from sqlalchemy.ext.asyncio import async_sessionmaker
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
        **kwargs,
    ) -> decl_api.DeclarativeBase:
        session_maker = getattr(
            cls._meta,
            "sqlalchemy_session_factory",
            None,
        )
        assert (  # noqa: F631
            isinstance(session_maker, async_sessionmaker),
            f"{cls.__name__}.Meta.sessionmaker must be"
            f" {async_sessionmaker.__name__}, not {type(session_maker)}",
        )
        instance: decl_api.DeclarativeBase = model_class(*args, **kwargs)
        async with session_maker() as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
        return instance

    @classmethod
    async def create_batch(
        cls,
        size: int,
        session: asyncio_ext.AsyncSession,
        **kwargs,
    ):
        return [await cls(session=session, **kwargs) for _ in range(size)]
