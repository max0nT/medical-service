from dishka import Provider, Scope, provide
from fastapi_storages import S3Storage

from app.features.s3.upload.handler import UploadS3FileHandler
from lib.model.fields import S3Backend


class UploadS3FileProvider(Provider):
    """Provider class for upload s3 file handler."""

    scope = Scope.REQUEST

    handler = provide(UploadS3FileHandler, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    def get_s3_backend(self) -> S3Storage:
        """Return configured s3 backend."""
        return S3Backend
