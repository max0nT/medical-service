from dishka import Provider, Scope, provide

from app.features.users.update.handler import UpdateUserHandler
from app.features.users.update.repository import UserRepository


class UpdateUserProvider(Provider):
    """Provider class for update user handler."""

    scope = Scope.REQUEST

    handler = provide(UpdateUserHandler, scope=Scope.REQUEST)
    user_repo = provide(UserRepository, scope=Scope.REQUEST)
