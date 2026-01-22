import httpx

from src import models

from .base import BasePermission


class IsAuthenticatedPermission(BasePermission):
    status_code = httpx.codes.UNAUTHORIZED

    def has_permissions(self) -> bool:
        return isinstance(
            self.request.user,
            models.User,
        )
