import typing

from app.domain.entities.user import User
from app.features.users.list.command import ListUsersCommand
from app.features.users.list.repository import UserRepository
from lib.fastapi.permissions import IsAuthenticatedPermission
from lib.protocols import HandlerProtocol


class ListUsersHandler(HandlerProtocol):
    """Handler to return list of users."""

    permissions = (IsAuthenticatedPermission,)

    def __init__(
        self,
        user_repo: UserRepository,
    ) -> None:
        self.user_repo = user_repo

    async def __call__(
        self,
        command: ListUsersCommand,
        **kwargs,
    ) -> typing.Sequence[User]:
        """Call handler."""
        return await self.user_repo.select_users(
            limit=command.limit,
            offset=command.offset,
            ordering=command.ordering,
            role=command.role,
        )
