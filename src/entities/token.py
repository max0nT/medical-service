import pydantic


class AuthToken(pydantic.BaseModel):
    """Describe schema for jwt auth token."""

    access_token: str
