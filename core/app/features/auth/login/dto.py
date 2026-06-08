import pydantic


class LoginDTO(pydantic.BaseModel):
    """DTO class for login handler."""

    email: str
    password: str


class AccessToken(pydantic.BaseModel):
    """DTO class with jwt token data."""

    access_token: str
