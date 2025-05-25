import enum

import sqlalchemy

from .core import BaseModel


class User(BaseModel):
    """Model to describe user keeping data."""

    __tablename__ = "users"

    email = sqlalchemy.Column(
        name="email",
        type_=sqlalchemy.String(255),
        nullable=False,
        unique=True,
    )
    first_name = sqlalchemy.Column(
        name="first_name",
        type_=sqlalchemy.String(255),
        nullable=True,
    )
    last_name = sqlalchemy.Column(
        name="last_name",
        type_=sqlalchemy.String(255),
        nullable=True,
    )
    password = sqlalchemy.Column(
        name="password",
        type_=sqlalchemy.String(255),
    )
    sync_with_google_calendar = sqlalchemy.Column(
        name="sync_with_google_calendar",
        type_=sqlalchemy.Boolean(),
        default=False,
    )

    class Role(enum.StrEnum):
        """User's roles in system."""

        employee = enum.auto()
        client = enum.auto()
        admin = enum.auto()

    role = sqlalchemy.Column(
        name="role",
        type_=sqlalchemy.Enum(Role),
        default=Role.client,
    )
