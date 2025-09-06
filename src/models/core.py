import enum

import sqlalchemy

from config import settings


class OnDelete(enum.StrEnum):
    """Describe values for `on_delete` options.

    Unlike django or, sqlalchemy doesn't provide enum to describe
    `on_delete` option values.
    See also https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK


    """

    CASCADE = "CASCADE"
    RESTRICT = "RESTRICT"
    SET_NULL = "SET NULL"


class BaseModel(settings.Base):
    """Mode to setup base fields such as id, created, modified."""

    __abstract__ = True

    id = sqlalchemy.Column(
        name="id",
        type_=sqlalchemy.Integer(),
        autoincrement=True,
        nullable=False,
        primary_key=True,
    )
    created = sqlalchemy.Column(
        name="created",
        type_=sqlalchemy.DateTime(),
        server_default=sqlalchemy.func.now(),
    )
    modified = sqlalchemy.Column(
        name="modified",
        type_=sqlalchemy.DateTime(),
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now(),
    )

    async def refresh_from_db(self) -> None:
        """Refresh instance from db."""
        async with settings.session_factory() as session:
            session.add(self)
            await session.refresh(self)
