from dishka import Provider, Scope, provide

from lib.jwt import JWTService


class JwtProvider(Provider):
    """Provider class for jwt service."""

    scope = Scope.REQUEST

    jwt_service = provide(JWTService, scope=Scope.REQUEST)
