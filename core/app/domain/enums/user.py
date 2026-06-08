import enum


class Role(enum.StrEnum):
    """User's roles in system."""

    employee = enum.auto()
    client = enum.auto()
    admin = enum.auto()
