import functools
import typing

import fastapi

import httpx

from src import models


class BasePermission:
    """Base API permission class."""

    error_message = "You don't have permissions to perform that action"
    status_code = httpx.codes.FORBIDDEN

    def __init__(
        self,
        user: models.User | None = None,
        **kwargs,
    ):
        self.user = user
        self.kwargs = kwargs

    def has_permissions(self) -> bool:
        """Check there are enough permission to perform the action."""
        return True


def permission_list(permission_classes: typing.Iterable[BasePermission] = ()):
    def outer_wrapper(func):
        @functools.wraps(func)
        async def wrap(*args, **kwargs):
            for permission in permission_classes:
                assert (  # noqa: F631
                    isinstance(permission, BasePermission),
                    f"Permission class must be {BasePermission},"
                    f" not {permission.__class__.__name__}",
                )
                permission_obj = permission(**kwargs)
                if not permission_obj.has_permissions():
                    raise fastapi.HTTPException(
                        status_code=permission_obj.status_code,
                        detail={
                            "detail": permission_obj.error_message,
                        },
                    )
            return await func(*args, **kwargs)

        return wrap

    return outer_wrapper
