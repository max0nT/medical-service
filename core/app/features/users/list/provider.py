from dishka import Provider, Scope, provide

from app.features.users.list.handler import ListUsersHandler
from app.features.users.list.repository import UserRepository
from lib.protocols import HandlerProtocol


class ListUsersProvider(Provider):
    """Provider class for list users handler."""

    scope = Scope.REQUEST

    handler = provide(
        ListUsersHandler,
        provides=HandlerProtocol,
        scope=Scope.REQUEST,
    )
    user_repo = provide(UserRepository, scope=Scope.REQUEST)
