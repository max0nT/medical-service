from src import models

from .core import BaseRepository


class UserRepository(
    BaseRepository[models.User],
):
    """Repository class for `User` model."""

    model = models.User
