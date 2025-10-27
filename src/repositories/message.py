from src.models import Message

from .core import BaseRepository


class MessageRepository(BaseRepository[Message]):
    """Repository class for `Message` model."""

    model = Message
