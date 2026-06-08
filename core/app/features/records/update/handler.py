from app.domain.entities.record import Record
from app.features.records.update.command import UpdateRecordCommand
from app.features.records.update.repository import RecordRepository
from lib.fastapi.permissions import (
    IsAuthenticatedPermission,
    UserEmployeePermission,
)
from lib.protocols import HandlerProtocol


class UpdateRecordHandler(HandlerProtocol):
    """Handler to update record."""

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
        command: UpdateRecordCommand,
        **kwargs,
    ) -> Record:
        """Call handler."""
        return await self.record_repo.update_record(
            pk=command.pk,
            start=command.start,
            end=command.end,
        )
