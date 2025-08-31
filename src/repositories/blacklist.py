from src import models

from .core import BaseRepository


class BlackListRepository(BaseRepository[models.TokenBlackList]):
    model: type[models.TokenBlackList] = models.TokenBlackList
