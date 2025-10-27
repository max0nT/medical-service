from src.models import Chat

from .core import BaseRepository


class ChatRepository(BaseRepository[Chat]):
    """Repository class for `Chat` model."""

    model = Chat
