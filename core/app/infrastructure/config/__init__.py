import pydantic_settings

from lib.config.auth import AuthSettings
from lib.config.database import PostgresSettings
from lib.config.rabbitmq import RabbitMqSettings
from lib.config.redis import RedisSettings
from lib.config.s3 import S3Config

from .qr import QrApiSettings


class Settings(
    AuthSettings,
    PostgresSettings,
    RabbitMqSettings,
    RedisSettings,
    QrApiSettings,
    S3Config,
):
    """Settings class for app."""

    model_config = pydantic_settings.SettingsConfigDict(
        extra="ignore",
        env_file=".env"
    )


settings = Settings()
