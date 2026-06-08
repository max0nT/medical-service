import fastapi

from app.domain.entities.user import User
from app.features.users.update.command import UpdateUserCommand
from app.features.users.update.repository import UserRepository
from lib.fastapi.permissions import IsAuthenticatedPermission
from lib.protocols import HandlerProtocol


class UpdateUserHandler(HandlerProtocol):
    """Handler to update user info."""

    permissions = (IsAuthenticatedPermission,)

    def __init__(
        self,
        user_repo: UserRepository,
    ) -> None:
        self.user_repo = user_repo

    async def __call__(
        self,
        command: UpdateUserCommand,
        **kwargs,
    ) -> User:
        """Call handler."""
        if command.current_user_id != command.pk:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_403_FORBIDDEN,
                detail={
                    "detail": "You can edit only yourself.",
                },
            )
        return await self.user_repo.update_user(
            pk=command.pk,
            first_name=command.first_name,
            last_name=command.last_name,
            sync_with_google_calendar=command.sync_with_google_calendar,
            avatar=command.avatar,
        )
