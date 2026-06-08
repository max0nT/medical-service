from app.domain.entities.user import User
from lib.repository.sa import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository class for `User` model."""

    async def update_user(
        self,
        *,
        pk: int,
        first_name: str | None,
        last_name: str | None,
        sync_with_google_calendar: bool,
        avatar: str | None,
    ) -> User:
        """Update user by primary key."""
        user = await self.select_one(pk=pk)
        user.first_name = first_name
        user.last_name = last_name
        user.sync_with_google_calendar = sync_with_google_calendar
        user.avatar = avatar

        return user
