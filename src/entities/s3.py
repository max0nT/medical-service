import pydantic


class S3Path(pydantic.BaseModel):
    """Base model to describe s3 path info."""

    path: pydantic.networks.AnyUrl
