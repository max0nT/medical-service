import typing

import pydantic


class UploadS3FileCommand(pydantic.BaseModel):
    """Command class for uploading file to s3."""

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    file: typing.BinaryIO
