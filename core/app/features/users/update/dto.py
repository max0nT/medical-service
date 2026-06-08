import pydantic


class UserUpdateDTO(pydantic.BaseModel):
    """DTO class for updating user info."""

    first_name: str | None
    last_name: str | None
    sync_with_google_calendar: bool
    avatar: str | None = None
