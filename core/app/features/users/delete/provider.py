from dishka import Provider, Scope, provide

from app.features.users.delete.handler import DeleteUserHandler
from app.features.users.delete.repository import UserRepository


class DeleteUserProvider(Provider):
    """Provider class for delete user handler."""

    scope = Scope.REQUEST

    handler = provide(DeleteUserHandler, scope=Scope.REQUEST)
    user_repo = provide(UserRepository, scope=Scope.REQUEST)
