from app.domain.entities.record import Record
from app.features.records.create.command import CreateRecordCommand
from app.features.records.create.repository import RecordRepository
from lib.fastapi.permissions import (
    IsAuthenticatedPermission,
    UserEmployeePermission,
)
from lib.protocols import HandlerProtocol


class CreateRecordHandler(HandlerProtocol):
    """Handler to create record."""

    permissions = (
        IsAuthenticatedPermission,
        UserEmployeePermission,
    )

    def __init__(
        self,
        record_repo: RecordRepository,
    ) -> None:
        self.record_repo = record_repo

    async def __call__(
        self,
        command: CreateRecordCommand,
        **kwargs,
    ) -> Record:
        """Call handler."""
        return await self.record_repo.create_record(
            created_by_id=command.created_by_id,
            start=command.start,
            end=command.end,
        )
