import typing

import fastapi

from app.domain.entities.user import User


class Request(fastapi.Request):
    """Request class which allows to keep info about user for API request."""

    def __init__(self, user: User | None = None, **kwargs):
        self._user = user
        super().__init__(
            scope=kwargs["scope"],
            receive=kwargs["_receive"],
            send=kwargs["_send"],
        )
        self.scope["user"] = user


def get_request(request: fastapi.Request) -> Request:
    """Return project request class with authenticated user in scope."""
    return typing.cast(Request, request)
