import fastapi

from app.features.users.delete.command import DeleteUserCommand
from app.features.users.delete.repository import UserRepository
from lib.fastapi.permissions import IsAuthenticatedPermission
from lib.protocols import HandlerProtocol


class DeleteUserHandler(HandlerProtocol):
    """Handler to delete user."""

    permissions = (IsAuthenticatedPermission,)

    def __init__(
        self,
        user_repo: UserRepository,
    ) -> None:
        self.user_repo = user_repo

    async def __call__(
        self,
        command: DeleteUserCommand,
        **kwargs,
    ) -> None:
        """Call handler."""
        if command.current_user_id != command.pk:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_403_FORBIDDEN,
                detail={
                    "detail": "You can delete only yourself.",
                },
            )

        user = await self.user_repo.select_one(pk=command.pk)
        await self.user_repo.delete_user(user=user)
