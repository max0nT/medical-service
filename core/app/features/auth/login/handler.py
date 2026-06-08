import arrow

from app.features.auth.login.command import LoginCommand
from app.features.auth.login.repository import UserRepository
from app.infrastructure.config import Settings
from lib.exceptions import ObjectNotFoundException
from lib.jwt import JwtPayload, JWTService
from lib.password import ARGO2PasswordHasher
from lib.protocols import HandlerProtocol


class LoginHandler(HandlerProtocol):
    """Handler to implement user login."""

    def __init__(
        self,
        password_hasher: ARGO2PasswordHasher,
        user_repo: UserRepository,
        jwt_service: JWTService,
        settings: Settings,
    ) -> None:
        self.password_hasher = password_hasher
        self.user_repo = user_repo
        self.jwt_service = jwt_service
        self.settings = settings

    async def __call__(self, command: LoginCommand, **kwargs) -> str:
        """Call handler."""
        user_list = await self.user_repo.select(
            email=command.email,
        )
        if not user_list:
            raise ObjectNotFoundException(
                "User with that email and password doesn't exist.",
            )

        user = user_list[0]
        if not self.password_hasher.verify(user.password, command.password):
            raise ObjectNotFoundException(
                "User with that email and password doesn't exist.",
            )

        token = self.jwt_service.setup_token(
            payload=JwtPayload(
                id=user.id,
                exp=arrow.utcnow().shift(
                    minutes=self.settings.access_token_expire_minutes,
                ),
            ),
        )

        return token
