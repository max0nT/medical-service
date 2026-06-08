import datetime

import pydantic

from app.domain.enums.user import Role


class UserReadDTO(pydantic.BaseModel):
    """DTO class to represent user info."""

    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    created: datetime.datetime
    modified: datetime.datetime
    email: str
    first_name: str | None
    last_name: str | None
    sync_with_google_calendar: bool
    role: Role
    avatar: str | None
