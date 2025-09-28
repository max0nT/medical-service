import boto3

from config import settings


class S3Client:
    """Class for interaction with s3 storage."""

    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.endpoint_url,
            aws_access_key_id=settings.aws_access_key_id,
            aws_access_secret_key=settings.aws_access_secret_key,
        )
