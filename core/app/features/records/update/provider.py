from dishka import Provider, Scope, provide

from app.features.records.update.handler import UpdateRecordHandler
from app.features.records.update.repository import RecordRepository


class UpdateRecordProvider(Provider):
    """Provider class for update record handler."""

    scope = Scope.REQUEST

    handler = provide(UpdateRecordHandler, scope=Scope.REQUEST)
    record_repo = provide(RecordRepository, scope=Scope.REQUEST)
