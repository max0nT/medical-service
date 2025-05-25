import http
import typing

import arrow
import fastapi
import jwt
from passlib.context import CryptContext

import config
from src import entities, models, repositories

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthClient:
    """Provide base logic with signing in/up and authentication."""

    @classmethod
    def create_auth_client(cls) -> typing.Self:
        """Init Auth client instance."""
        return cls()

    async def sign_up(
        self,
        data: entities.UserSignUpSchema,
    ) -> tuple[str, models.User]:
        """Create user logic."""
        repository = await repositories.UserRepository.create_repository()
        check_exist = await repository.get_list(email=data.email)
        if check_exist:
            raise fastapi.HTTPException(
                status_code=http.HTTPStatus.BAD_REQUEST,
                detail={"detail": f"User with email {data.email} already exists"},
            )
        if (
            not (data.password and data.password_repeat)
            and data.password != data.password_repeat
        ):
            raise fastapi.HTTPException(
                status_code=http.HTTPStatus.BAD_REQUEST,
                detail={"detail": "Passwords don't match"},
            )
        hashed_password = self.hash_password(password=data.password)
        user = await repository.create_one(
            email=data.email,
            password=hashed_password,
            role=models.User.Role.client.value,
        )
        token = self.setup_token(user=user)
        return token, user

    async def authenticate(self, data: entities.UserSignInSchema) -> str:
        """Implement user signing in if all correct return access token."""
        repository = await repositories.UserRepository.create_repository()
        exception = fastapi.HTTPException(
            status_code=http.HTTPStatus.BAD_REQUEST,
            detail={"detail": "Wrong email or password."},
        )
        result_list = await repository.get_list()
        if not result_list:
            raise exception
        user = result_list[0]
        if not self.check_password(
            password=data.password,
            hashed_password=user.password,
        ):
            raise exception
        return self.setup_token(user=user)

    def hash_password(self, password: str) -> str:
        """Hash password."""
        return pwd_context.hash(password)

    def check_password(self, password: str, hashed_password: str) -> bool:
        """Check password is right."""
        return pwd_context.verify(password, hashed_password)

    def setup_token(self, user: models.User) -> str:
        """Setup access token."""
        data = {
            "id": user.id,
            "exp": arrow.utcnow()
            .shift(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
            .datetime,
        }
        token = jwt.encode(
            payload=data,
            key=config.SECRET_KEY,
            algorithm=config.ALGORITHM,
        )
        return token

    async def check_token_expired(self, token: str) -> bool:
        """Check that token in black list."""
        repository = await repositories.BlackListRepostitory.create_repository()
        is_expired = await repository.get_list(value=token)
        return bool(is_expired)

    def check_token_is_valid(self, token: str) -> int:
        """Check token is valid if yes return user id."""
        try:
            payload = jwt.decode(
                token,
                config.SECRET_KEY,
                [config.ALGORITHM],
            )
        except jwt.exceptions.InvalidTokenError:
            raise fastapi.HTTPException(
                status=http.HTTPStatus.UNAUTHORIZED,
                detail={
                    "detail": "Token is invalid",
                },
            )
        return payload.get("id")

    async def move_token_to_black_list(self, token: str) -> None:
        """Move JWT token to black list."""
        repository = await repositories.BlackListRepostitory.create_repository()
        await repository.create_one(value=token)
