from dishka import Provider, Scope, provide

from app.features.records.list.handler import ListRecordsHandler
from app.features.records.list.repository import RecordRepository


class ListRecordsProvider(Provider):
    """Provider class for list records handler."""

    scope = Scope.REQUEST

    handler = provide(ListRecordsHandler, scope=Scope.REQUEST)
    record_repo = provide(RecordRepository, scope=Scope.REQUEST)
