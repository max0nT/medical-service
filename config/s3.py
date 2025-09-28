import pydantic_settings


class S3Config(pydantic_settings.BaseSettings):
    """Config for s3 storage."""

    endpoint_url: str
    aws_access_key_id: str
    aws_access_secret_key: str
