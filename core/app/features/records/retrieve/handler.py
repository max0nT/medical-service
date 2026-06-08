from app.domain.entities.record import Record
from app.features.records.retrieve.command import RetrieveRecordCommand
from app.features.records.retrieve.repository import RecordRepository
from lib.fastapi.permissions import IsAuthenticatedPermission
from lib.protocols import HandlerProtocol


class RetrieveRecordHandler(HandlerProtocol):
    """Handler to retrieve record."""

    permissions = (IsAuthenticatedPermission,)

    def __init__(
        self,
        record_repo: RecordRepository,
    ) -> None:
        self.record_repo = record_repo

    async def __call__(
        self,
        command: RetrieveRecordCommand,
        **kwargs,
    ) -> Record:
        """Call handler."""
        return await self.record_repo.select_one(pk=command.pk)
