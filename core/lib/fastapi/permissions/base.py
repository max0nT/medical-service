import functools
import typing

import fastapi

import httpx


class BasePermission:
    """Base API permission class."""

    error_message = "You don't have permissions to perform that action"
    status_code = httpx.codes.FORBIDDEN

    def __init__(
        self,
        request: fastapi.Request | None = None,
        **kwargs,
    ):
        assert isinstance(
            request,
            fastapi.Request,
        ), (
            f"Request objects must be {fastapi.Request},"
            f" not {request.__class__.__name__}"
        )
        self.request = request
        self.kwargs = kwargs

    def has_permissions(self) -> bool:
        """Check there are enough permission to perform the action."""
        return True


def permission_list(
    permission_classes: typing.Iterable[type[BasePermission]] = (),
):
    def outer_wrapper(func):
        @functools.wraps(func)
        async def wrap(*args, **kwargs):
            for permission in permission_classes:
                assert issubclass(
                    permission,
                    BasePermission,
                ), (
                    f"Permission class must be {BasePermission},"
                    f" not {permission.__name__}"
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
