from dishka import Provider, Scope, provide

from app.features.records.create.handler import CreateRecordHandler
from app.features.records.create.repository import RecordRepository


class CreateRecordProvider(Provider):
    """Provider class for create record handler."""

    scope = Scope.REQUEST

    handler = provide(CreateRecordHandler, scope=Scope.REQUEST)
    record_repo = provide(RecordRepository, scope=Scope.REQUEST)
