import enum
import typing

import sqlalchemy
import sqlalchemy.orm as orm
from fastapi_storages import S3Storage

from config import settings


def get_s3_backend() -> S3Storage:
    """Get S3 backend for models."""
    S3Storage.AWS_ACCESS_KEY_ID = settings.aws_access_key_id
    S3Storage.AWS_SECRET_ACCESS_KEY = settings.aws_access_secret_key
    S3Storage.AWS_S3_USE_SSL = settings.use_ssl
    S3Storage.AWS_S3_ENDPOINT_URL = settings.endpoint_url
    S3Storage.AWS_S3_BUCKET_NAME = settings.bucket_name
    return S3Storage()


s3_backend = get_s3_backend()


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

    @property
    def model_name(self) -> type[typing.Self]:
        return self.__class__

    async def refresh_from_db(self) -> None:
        """Refresh instance from db."""
        async with settings.session_factory() as session:
            session.add(self)
            await session.refresh(self)

    async def joined_load(self, *relationships) -> typing.Self:
        async with settings.session_factory() as session:
            raw = await session.execute(
                sqlalchemy.select(self.model_name)
                .options(orm.joinedload(*relationships))
                .filter_by(id=self.id),
            )
            instance = raw.scalar_one()
        return instance
