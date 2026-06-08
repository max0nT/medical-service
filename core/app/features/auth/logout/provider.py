from dishka import Provider, Scope, provide

from app.features.auth.logout.handler import LogoutHandler


class LogoutProvider(Provider):
    """Provider class for logout handler."""

    scope = Scope.REQUEST

    handler = provide(LogoutHandler, scope=Scope.REQUEST)
