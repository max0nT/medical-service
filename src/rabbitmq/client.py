import enum

import aio_pika

from config import settings

from src import entities


class RoutingKeys(enum.StrEnum):
    """Enum of available routing keys."""

    EMAIL_SIGN_UP = "email.sign_up"
    EMAIL_RESERVE = "email.reserve"


class Exchanges(enum.StrEnum):
    """Enum of available exchanges."""

    EMAIL = "email_exchange"


class RabbitMqClient:
    """RabbitMq client for sending messages."""

    @staticmethod
    async def send_message(
        body_message: entities.BaseEmailBody,
        queue: RoutingKeys,
        exchange: Exchanges,
    ) -> None:
        """Send message."""
        conn = await aio_pika.connect_robust(settings.amqp_url)
        ch = await conn.channel()
        ch.get_exchange(exchange)
        await ch.default_exchange.publish(
            message=aio_pika.Message(
                body=bytes(
                    body_message.model_dump_json(),
                    encoding="utf-8",
                ),
            ),
            routing_key=queue,
        )
        await ch.close()
