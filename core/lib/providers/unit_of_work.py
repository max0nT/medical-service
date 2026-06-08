from dishka import Provider, Scope, decorate

from lib.protocols import HandlerProtocol
from lib.unit_of_work import UnitOfWorkHandler


class UnitOfWorkProvider(Provider):
    """Provider for `unit of work` decorator."""

    scope = Scope.REQUEST

    uow = decorate(
        UnitOfWorkHandler,
        provides=HandlerProtocol,
        scope=Scope.REQUEST,
    )
