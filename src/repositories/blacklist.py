from src import models

from .core import BaseRepository


class BlackListRepostitory(BaseRepository[models.TokenBlackList]):
    model: type[models.TokenBlackList] = models.TokenBlackList
