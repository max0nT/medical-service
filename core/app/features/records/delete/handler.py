from app.features.records.delete.command import DeleteRecordCommand
from app.features.records.delete.repository import RecordRepository
from lib.fastapi.permissions import (
    IsAuthenticatedPermission,
    UserEmployeePermission,
)
from lib.protocols import HandlerProtocol


class DeleteRecordHandler(HandlerProtocol):
    """Handler to delete record."""

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
        command: DeleteRecordCommand,
        **kwargs,
    ) -> None:
        """Call handler."""
        await self.record_repo.delete_record(pk=command.pk)
