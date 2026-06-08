from app.domain.entities.user import User
from lib.repository.sa import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository class for `User` model."""
