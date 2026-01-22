import typing

from src.repositories.core import REPO_CLASSES, BaseRepository

T = typing.TypeVar("T")


def get_repo(modelClass: T) -> BaseRepository[T]:
    """Return repo corresponding to model"""

    def wrapper():
        # Model may have own repository class
        if modelClass in REPO_CLASSES:
            return REPO_CLASSES[modelClass](model=modelClass)
        return BaseRepository[modelClass](model=modelClass)

    return wrapper
