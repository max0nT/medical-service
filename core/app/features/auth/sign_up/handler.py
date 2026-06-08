import fastapi

from app.domain.entities.user import User
from app.domain.enums.user import Role
from app.domain.events.email import EmailSignUpBody
from app.features.auth.sign_up.command import SignUpCommand
from app.features.auth.sign_up.repository import UserRepository
from lib.broker.rabbit import Exchanges, RabbitMqClient, RoutingKeys
from lib.password import ARGO2PasswordHasher
from lib.protocols import HandlerProtocol


class SignUpHandler(HandlerProtocol):
    """Handler to implement user sign up."""

    def __init__(
        self,
        password_hasher: ARGO2PasswordHasher,
        user_repo: UserRepository,
        rabbitmq_broker: RabbitMqClient,
    ) -> None:
        self.password_hasher = password_hasher
        self.user_repo = user_repo
        self.rabbitmq_client = rabbitmq_broker

    async def __call__(
        self,
        command: SignUpCommand,
        **kwargs,
    ) -> User:
        """Call handler."""

        existing_users = await self.user_repo.select(email=command.email)
        if existing_users:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                detail=f"User with email {command.email} already exists",
            )
        user = User(
            email=command.email,
            password=self.password_hasher.hash(command.password),
            role=Role.client,
        )
        await self.user_repo.add(user, flush=True)
        await self.rabbitmq_client.send_message(
            body_message=EmailSignUpBody(email=user.email),
            queue=RoutingKeys.EMAIL_SIGN_UP,
            exchange=Exchanges.EMAIL,
        )
        return user
