from dishka import Provider, Scope, provide

from lib.password import ARGO2PasswordHasher


class PasswordHasherProvider(Provider):
    """Provider class for password hasher."""

    scope = Scope.REQUEST

    hasher = provide(ARGO2PasswordHasher, scope=Scope.REQUEST)
