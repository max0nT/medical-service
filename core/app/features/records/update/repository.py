from app.domain.entities.record import Record
from lib.repository.sa import BaseRepository


class RecordRepository(BaseRepository[Record]):
    """Repository class for `Record` model."""

    async def update_record(
        self,
        *,
        pk: int,
        start,
        end,
    ) -> Record:
        """Update record by primary key."""
        record = await self.select_one(pk=pk)
        record.start = start
        record.end = end
        return record
