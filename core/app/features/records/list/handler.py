import typing

from app.domain.entities.record import Record
from app.features.records.list.command import ListRecordsCommand
from app.features.records.list.repository import RecordRepository
from lib.fastapi.permissions import IsAuthenticatedPermission
from lib.protocols import HandlerProtocol


class ListRecordsHandler(HandlerProtocol):
    """Handler to return list of records."""

    permissions = (IsAuthenticatedPermission,)

    def __init__(
        self,
        record_repo: RecordRepository,
    ) -> None:
        self.record_repo = record_repo

    async def __call__(
        self,
        command: ListRecordsCommand,
        **kwargs,
    ) -> typing.Sequence[Record]:
        """Call handler."""
        return await self.record_repo.select_records(
            created_by_id=command.created_by,
            reserved_by_id=command.reserved_by,
        )
