import httpx

from app.domain.entities.user import User
from app.domain.enums.user import Role
from lib.fastapi.permissions.base import BasePermission


class IsAuthenticatedPermission(BasePermission):
    """Permission class to check user is authenticated."""

    error_message = "Unauthorized"
    status_code = httpx.codes.UNAUTHORIZED

    def has_permissions(self) -> bool:
        """Check user is authenticated."""
        return isinstance(self.request.scope.get("user"), User)


class UserEmployeePermission(BasePermission):
    """Permission class to check user is employee."""

    def has_permissions(self) -> bool:
        """Check user has employee role."""
        user = self.request.scope.get("user")
        return isinstance(user, User) and user.role == Role.employee


class UserClientPermission(BasePermission):
    """Permission class to check user is client."""

    def has_permissions(self) -> bool:
        """Check user has client role."""
        user = self.request.scope.get("user")
        return isinstance(user, User) and user.role == Role.client
