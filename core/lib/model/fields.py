import typing

from fastapi_storages import S3Storage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy.engine.interfaces import Dialect

from app.infrastructure.config import settings


class S3FileType(FileType):
    """Extended class for s3 file storage.

    Allows to use string path to insert image url into database.

    """

    def process_bind_param(self, value: typing.Any, dialect: Dialect):
        """Save image in database.

        Allow to process with url path.

        """
        if isinstance(value, str):
            return value
        return super().process_bind_param(value, dialect)


def get_s3_backend() -> S3Storage:
    """Get S3 backend for models."""
    S3Storage.AWS_ACCESS_KEY_ID = settings.aws_access_key_id
    S3Storage.AWS_SECRET_ACCESS_KEY = settings.aws_access_secret_key
    S3Storage.AWS_S3_USE_SSL = settings.use_ssl
    S3Storage.AWS_S3_ENDPOINT_URL = settings.endpoint_url
    S3Storage.AWS_S3_BUCKET_NAME = settings.bucket_name
    S3Storage.AWS_QUERYSTRING_AUTH = True
    return S3Storage()


S3Backend = get_s3_backend()
