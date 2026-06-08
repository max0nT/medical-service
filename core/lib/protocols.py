import typing

from lib.fastapi.permissions.base import BasePermission


class HandlerProtocol(typing.Protocol):
    """Protocol to describe handler which is responsible for feature exec."""

    permissions: tuple[type[BasePermission], ...] = ()
