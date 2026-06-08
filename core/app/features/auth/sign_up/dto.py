import typing

import pydantic

from app.domain.enums.user import Role


class SignUpDTO(pydantic.BaseModel):
    """DTO class for sign up handler."""

    email: str
    password: str
    password_repeat: str

    @pydantic.model_validator(mode="after")
    def password_match(self) -> typing.Self:
        """Check passwords are match."""
        if self.password != self.password_match:
            raise ValueError("Passwords are not match")
        return self


class SignUpResponseDTO(pydantic.BaseModel):
    """Dto class for signup response."""

    model_config = pydantic.ConfigDict(from_attributes=True)

    email: str
    first_name: str | None
    last_name: str | None
    sync_with_google_calendar: bool
    role: Role
    avatar: str | None
