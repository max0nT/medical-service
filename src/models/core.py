import sqlalchemy

import config as settings


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
