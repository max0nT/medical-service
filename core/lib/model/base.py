import enum

import sqlalchemy
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class OnDelete(enum.StrEnum):
    """Describe values for `on_delete` options.

    Unlike django or, sqlalchemy doesn't provide enum to describe
    `on_delete` option values.
    See also https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK


    """

    CASCADE = "CASCADE"
    RESTRICT = "RESTRICT"
    SET_NULL = "SET NULL"


class BaseModel(Base):
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
