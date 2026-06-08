from dishka import Provider, Scope, provide

from app.features.records.reserve.handler import ReserveRecordHandler
from app.features.records.reserve.qr import QRCodeClient, QrCodeGenerator
from app.features.records.reserve.repository import RecordRepository
from lib.broker.rabbit import RabbitMqClient


class ReserveRecordProvider(Provider):
    """Provider class for reserve record handler."""

    scope = Scope.REQUEST

    handler = provide(ReserveRecordHandler, scope=Scope.REQUEST)
    record_repo = provide(RecordRepository, scope=Scope.REQUEST)
    qr_code_client = provide(QRCodeClient, scope=Scope.REQUEST)
    qr_code_generator = provide(QrCodeGenerator, scope=Scope.REQUEST)
    rabbitmq_broker = provide(RabbitMqClient, scope=Scope.REQUEST)
