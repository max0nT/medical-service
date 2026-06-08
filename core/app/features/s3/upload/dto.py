import pydantic


class S3PathDTO(pydantic.BaseModel):
    """DTO class to describe s3 path info."""

    name: str
