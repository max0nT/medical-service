import functools

import pydantic_settings


class RabbitMqSettings(pydantic_settings.BaseSettings):
    """Class for RabbitMq settings."""

    rabbitmq_user: str
    rabbitmq_password: str
    rabbitmq_port: str

    @functools.cached_property
    def amqp_url(self) -> str:
        return (
            f"amqp://{self.rabbitmq_user}:"
            f"{self.rabbitmq_password}@rabbitmq:{self.rabbitmq_port}"
        )
