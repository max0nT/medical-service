from dishka import Provider, Scope, provide

from app.features.auth.login.handler import LoginHandler
from app.features.auth.login.repository import UserRepository


class LoginProvider(Provider):
    """Provider class for login handler."""

    scope = Scope.REQUEST

    handler = provide(LoginHandler, scope=Scope.REQUEST)
    user_repo = provide(UserRepository, scope=Scope.REQUEST)
