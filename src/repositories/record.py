from src import models

from .core import BaseRepository


class RecordRepository(
    BaseRepository[models.Record],
):
    """Repository class for `Record` model."""

    model: type[models.Record] = models.Record
