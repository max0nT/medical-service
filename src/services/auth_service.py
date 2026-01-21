import datetime
import http

import fastapi

import arrow
import jwt

from config import settings

from src import entities, models, protocols, repositories
from src.rabbitmq import rabbitmq_client
from src.redis.client import RedisAPIClient


class AuthClient:
    """Provide base logic with signing in/up and authentication."""

    def __init__(self, password_hasher: protocols.PasswordHasher) -> None:
        self.password_hasher = password_hasher

    async def sign_up(
        self,
        data: entities.UserSignUpSchema,
    ) -> tuple[str, models.User]:
        """Create user logic."""
        repo = await repositories.UserRepository.create_repository()
        check_exist = await repo.get_list(email=data.email)
        validations_errors = []
        if check_exist:
            validations_errors.append(
                f"User with email {data.email} already exists",
            )
        if (
            data.password
            and data.password_repeat
            and data.password != data.password_repeat
        ):
            validations_errors.append("Passwords don't match")

        if validations_errors:
            raise fastapi.HTTPException(
                status_code=http.HTTPStatus.BAD_REQUEST,
                detail={"detail": validations_errors[0]},
            )
        user = await repo.create_one(
            email=data.email,
            password=self.password_hasher.hash(data.password),
            role=models.User.Role.client.value,
        )
        token = self.setup_token(user=user)
        await rabbitmq_client.send_message(
            msg=(entities.EmailSignUp.model_validate(user).model_dump_json()),
            queue="email_notifications",
        )
        return token, user

    async def authenticate(self, data: entities.UserSignInSchema) -> str:
        """Implement user signing in if all correct return access token."""
        repo = await repositories.UserRepository.create_repository()
        user = await repo.get_list(
            email=data.email,
        )
        if (
            not user
            or user
            and not self.password_hasher.verify(
                user[0].password,
                data.password,
            )
        ):
            raise fastapi.HTTPException(
                status_code=http.HTTPStatus.BAD_REQUEST,
                detail={"detail": "Wrong email or password."},
            )
        return self.setup_token(user=user[0])

    def setup_token(self, user: models.User) -> str:
        """Setup access token."""
        data = {
            "id": user.id,
            "exp": arrow.utcnow()
            .shift(minutes=settings.access_token_expire_minutes)
            .datetime,
        }
        token = jwt.encode(
            payload=data,
            key=settings.secret_key,
            algorithm=settings.algorithm,
        )
        return token

    async def check_token_expired(self, token: str) -> bool:
        """Check that token in black list."""
        async with RedisAPIClient() as client:
            is_expired = await client.get_value(name=token)

        return bool(is_expired)

    async def check_token_is_valid(self, token: str) -> int:
        """Check token is valid if yes return user id."""
        payload = dict()
        try:
            payload: dict = jwt.decode(
                token,
                settings.secret_key,
                [settings.algorithm],
            )
        except jwt.exceptions.InvalidTokenError:
            return None

        async with RedisAPIClient() as client:
            is_banned = bool(await client.get_value(name=token))

        return payload.get("id") if not is_banned else None

    async def move_token_to_black_list(self, token: str) -> None:
        """Move JWT token to black list."""
        async with RedisAPIClient() as client:
            await client.set_value(
                key=token,
                value="banned_token",
                exp=datetime.timedelta(
                    minutes=settings.access_token_expire_minutes,
                ),
            )
