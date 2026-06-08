import pydantic


class SignUpCommand(pydantic.BaseModel):
    """Command class for sign up handler."""

    email: str
    password: str
    password_repeat: str
