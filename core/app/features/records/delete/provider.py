from dishka import Provider, Scope, provide

from app.features.records.delete.handler import DeleteRecordHandler
from app.features.records.delete.repository import RecordRepository


class DeleteRecordProvider(Provider):
    """Provider class for delete record handler."""

    scope = Scope.REQUEST

    handler = provide(DeleteRecordHandler, scope=Scope.REQUEST)
    record_repo = provide(RecordRepository, scope=Scope.REQUEST)
