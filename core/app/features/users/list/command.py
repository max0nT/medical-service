import enum

import pydantic

from app.domain.enums.user import Role


class UserOrdering(enum.StrEnum):
    """Available ordering fields for users list."""

    id = "id"
    id_desc = "-id"
    email = "email"
    email_desc = "-email"
    created = "created"
    created_desc = "-created"
    modified = "modified"
    modified_desc = "-modified"
    role = "role"
    role_desc = "-role"


class ListUsersCommand(pydantic.BaseModel):
    """Command class for list users handler."""

    limit: int
    offset: int
    ordering: UserOrdering | None
    role: Role | None
