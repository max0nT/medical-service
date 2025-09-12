from src import models

from .base import BasePermission


class UserEmployeePermission(BasePermission):
    """Base Permission class to check user is employee."""

    error_message = "Only employee can perform the action"

    def has_permissions(self):
        return self.user.role == models.User.Role.employee


class UserClientPermission(BasePermission):
    """Base Permission class to check user is client."""

    error_message = "Only client can perform the action."

    def has_permissions(self):
        return self.user.role == models.User.Role.client
