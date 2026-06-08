from dishka import Provider, Scope, provide

from app.features.auth.sign_up.handler import SignUpHandler
from app.features.auth.sign_up.repository import UserRepository
from lib.broker.rabbit import RabbitMqClient


class SignUpProvider(Provider):
    """Provider class for sign up handler."""

    scope = Scope.REQUEST

    handler = provide(SignUpHandler, scope=Scope.REQUEST)
    user_repo = provide(UserRepository, scope=Scope.REQUEST)
    rabbitmq_broker = provide(RabbitMqClient, scope=Scope.REQUEST)
