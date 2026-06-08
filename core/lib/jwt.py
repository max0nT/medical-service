import datetime

import jwt
import pydantic

from lib.config.auth import AuthSettings
from lib.repository.redis import RedisAPIClient


class JwtPayload(pydantic.BaseModel):
    """Pydantic model to describe jwt payload."""

    id: int
    exp: datetime.datetime


class JWTService:
    """Class to handle jwt tokens."""

    def __init__(
        self,
        settings: AuthSettings,
        redis: RedisAPIClient,
    ) -> None:
        self.settings = settings
        self.redis = redis

    async def check_token_is_valid(self, token: str) -> int:
        """Check token is valid if yes return user id."""
        payload = dict()
        try:
            payload: dict = jwt.decode(
                token,
                self.settings.secret_key,
                [self.settings.algorithm],
            )
        except jwt.exceptions.InvalidTokenError:
            return None

        is_banned = await self.check_token_expired(token=token)
        if is_banned:
            raise jwt.exceptions.InvalidTokenError
        return payload.get("id") if not is_banned else None

    async def move_token_to_black_list(self, token: str) -> None:
        """Move JWT token to black list."""
        async with self.redis.client as client:
            await client.set(
                key=token,
                value="banned_token",
                exp=datetime.timedelta(
                    minutes=self.settings.access_token_expire_minutes,
                ),
            )

    async def check_token_expired(self, token: str) -> bool:
        """Check that token in black list."""
        async with self.redis.client as client:
            is_expired = await client.get(token)
        return bool(is_expired)

    def setup_token(self, payload: JwtPayload) -> str:
        """Setup access token."""
        token = jwt.encode(
            payload=payload.model_dump(mode="json"),
            key=self.settings.secret_key,
            algorithm=self.settings.algorithm,
        )
        return token
