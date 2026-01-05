import aio_pika

from config import settings


class RabbitMqClient:
    """RabbitMq client for sending messages."""

    @staticmethod
    async def send_message(
        msg: str,
        queue: str,
    ) -> None:
        """Send message."""
        conn = await aio_pika.connect_robust(settings.amqp_url)
        ch = await conn.channel()
        await ch.declare_queue(queue)
        await ch.default_exchange.publish(
            message=aio_pika.Message(body=msg.encode()),
            routing_key=queue,
        )
        await ch.close()
