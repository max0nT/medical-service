import pydantic


class UpdateUserCommand(pydantic.BaseModel):
    """Command class for updating user info."""

    pk: int
    current_user_id: int
    first_name: str | None
    last_name: str | None
    sync_with_google_calendar: bool
    avatar: str | None = None
