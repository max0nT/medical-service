import fastapi

from src import models


class Request(fastapi.Request):
    """Request class which allows to keep info about user for API request."""

    def __init__(self, user: models.User | None = None, **kwargs):
        self._user = user
        super().__init__(
            scope=kwargs["scope"],
            receive=kwargs["_receive"],
            send=kwargs["_send"],
        )
        self.scope["user"] = user
