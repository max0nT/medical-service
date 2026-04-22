from src.models import User

from .core import BaseModelSchema, BaseReadModelSchema


class UserReadSchema(BaseReadModelSchema):
    """Base schema to represent info from `User` model."""

    email: str
    first_name: str | None
    last_name: str | None
    sync_with_google_calendar: bool
    role: User.Role
    avatar: str | None


class UserWriteSchema(BaseModelSchema):
    """Model to editing `User` instances"""

    first_name: str | None
    last_name: str | None
    sync_with_google_calendar: bool
    avatar: str | None = None


class UserSignUpSchema(BaseModelSchema):
    """Model fro signing up."""

    email: str
    password: str
    password_repeat: str


class UserSignInSchema(BaseModelSchema):
    """Model for signing in."""

    email: str
    password: str
