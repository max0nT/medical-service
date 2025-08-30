import pydantic

from src.models import User

from .core import BaseReadModelSchema, BaseModelSchema


class UserReadSchema(BaseReadModelSchema):
    """Base schema to represent info from `User` model."""

    email: str
    first_name: str | None
    last_name: str | None
    sync_with_google_calendar: bool
    role: User.Role


class UserWriteSchema(pydantic.BaseModel):
    """Model to editing `User` instances"""

    email: str
    first_name: str | None
    last_name: str | None
    sync_with_google_calendar: bool


class UserSignUpSchema(BaseModelSchema):
    """Model fro signing up."""

    email: str
    password: str
    password_repeat: str


class UserSignInSchema(BaseModelSchema):
    """Model for signing in."""

    email: str
    password: str
