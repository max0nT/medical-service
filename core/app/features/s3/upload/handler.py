import datetime

from fastapi_storages import S3Storage

from app.features.s3.upload.command import UploadS3FileCommand
from lib.protocols import HandlerProtocol


class UploadS3FileHandler(HandlerProtocol):
    """Handler to upload file to s3."""

    def __init__(
        self,
        s3_backend: S3Storage,
    ) -> None:
        self.s3_backend = s3_backend

    async def __call__(
        self,
        command: UploadS3FileCommand,
        **kwargs,
    ) -> str:
        """Call handler."""
        return self.s3_backend.write(
            file=command.file,
            name=(
                "photo"
                f"{datetime.datetime.now().strftime('_%d_%m_%Y__%H_%M_%S')}"
            ),
        )
