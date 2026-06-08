from app.features.auth.logout.command import LogoutCommand
from lib.jwt import JWTService
from lib.protocols import HandlerProtocol


class LogoutHandler(HandlerProtocol):
    """Handler to implement user logout."""

    def __init__(
        self,
        jwt_service: JWTService,
    ) -> None:
        self.jwt_service = jwt_service

    async def __call__(self, command: LogoutCommand, **kwargs) -> None:
        """Call handler."""
        await self.jwt_service.move_token_to_black_list(token=command.token)
