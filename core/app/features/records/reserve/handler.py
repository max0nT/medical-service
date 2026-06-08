import fastapi

from app.domain.entities.record import Record
from app.domain.events.email import EmailReservedBody
from app.features.records.reserve.command import ReserveRecordCommand
from app.features.records.reserve.qr import QrCodeGenerator
from app.features.records.reserve.repository import RecordRepository
from lib.broker.rabbit import Exchanges, RabbitMqClient, RoutingKeys
from lib.fastapi.permissions import (
    IsAuthenticatedPermission,
    UserClientPermission,
)
from lib.protocols import HandlerProtocol


class ReserveRecordHandler(HandlerProtocol):
    """Handler to reserve record."""

    permissions = (
        IsAuthenticatedPermission,
        UserClientPermission,
    )

    def __init__(
        self,
        record_repo: RecordRepository,
        qr_code_generator: QrCodeGenerator,
        rabbitmq_broker: RabbitMqClient,
    ) -> None:
        self.record_repo = record_repo
        self.qr_code_generator = qr_code_generator
        self.rabbitmq_client = rabbitmq_broker

    async def __call__(
        self,
        command: ReserveRecordCommand,
        **kwargs,
    ) -> Record:
        """Call handler."""
        record = await self.record_repo.reserve_record(pk=command.pk)
        if (
            record.reserved_by_id is not None
            and record.reserved_by_id != command.user_id
        ):
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                detail={"detail": "Record was reserved"},
            )

        record.reserved_by_id = (
            None
            if record.reserved_by_id == command.user_id
            else command.user_id
        )

        if record.reserved_by_id:
            record.qr_code = await self.qr_code_generator.generate(
                user_id=command.user_id,
            )
            record.email = command.user_email
            await self.rabbitmq_client.send_message(
                body_message=EmailReservedBody.model_validate(record),
                queue=RoutingKeys.EMAIL_RESERVE,
                exchange=Exchanges.EMAIL,
            )

        return record
