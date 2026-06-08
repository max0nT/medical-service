import pydantic


class LoginCommand(pydantic.BaseModel):
    """Command class for login handler."""

    email: str
    password: str
