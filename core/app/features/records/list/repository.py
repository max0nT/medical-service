import typing

from app.domain.entities.record import Record
from lib.repository.sa import BaseRepository


class RecordRepository(BaseRepository[Record]):
    """Repository class for `Record` model."""

    async def select_records(
        self,
        *,
        created_by_id: int | None = None,
        reserved_by_id: int | None = None,
    ) -> typing.Sequence[Record]:
        """Return records with optional filters."""
        filters = {}
        if created_by_id is not None:
            filters["created_by_id"] = created_by_id
        if reserved_by_id is not None:
            filters["reserved_by_id"] = reserved_by_id

        return await self.select(**filters)
