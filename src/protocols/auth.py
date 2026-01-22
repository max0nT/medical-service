from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from src import entities, models


class PasswordHasher(Protocol):
    """Interface to describe objects for password hashing."""

    def hash(self, password: str) -> str:
        """Return password hash."""

    def verify(self, hashed: str, password: str) -> bool:
        """Check password is compatible with some hash."""


class AuthClientProtocol(Protocol):
    """Protocol to describe auth client."""

    def __init__(self, password_hasher: PasswordHasher) -> None:
        pass

    async def sign_up(
        self,
        session: AsyncSession,
        data: entities.UserSignUpSchema,
    ) -> tuple[str, models.User]:
        """Create user logic."""

    async def authenticate(
        self,
        session: AsyncSession,
        data: entities.UserSignInSchema,
    ) -> str:
        """Implement user signing in if all correct return access token."""

    def setup_token(self, user: models.User) -> str:
        """Setup access token."""

    async def check_token_expired(self, token: str) -> bool:
        """Check that token in black list."""

    async def check_token_is_valid(self, token: str) -> int:
        """Check token is valid if yes return user id."""

    async def move_token_to_black_list(self, token: str) -> None:
        """Move JWT token to black list."""
