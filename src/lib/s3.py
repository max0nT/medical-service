from fastapi_storages import S3Storage

from config import settings


class AdvancedS3backend(S3Storage):
    """S3 backend with specified settings."""

    AWS_ACCESS_KEY_ID = settings.aws_access_key_id
    AWS_SECRET_ACCESS_KEY = settings.aws_access_secret_key
    AWS_S3_USE_SSL = settings.use_ssl
    AWS_S3_ENDPOINT_URL = settings.endpoint_url
    AWS_S3_BUCKET_NAME = settings.bucket_name
    AWS_QUERYSTRING_AUTH = settings.aws_querystring_auth


s3_backend = AdvancedS3backend()
