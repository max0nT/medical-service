import pydantic


class LogoutCommand(pydantic.BaseModel):
    """Command class for logout handler."""

    token: str
