from dishka import Provider, Scope, provide

from app.features.records.retrieve.handler import RetrieveRecordHandler
from app.features.records.retrieve.repository import RecordRepository


class RetrieveRecordProvider(Provider):
    """Provider class for retrieve record handler."""

    scope = Scope.REQUEST

    handler = provide(RetrieveRecordHandler, scope=Scope.REQUEST)
    record_repo = provide(RecordRepository, scope=Scope.REQUEST)
