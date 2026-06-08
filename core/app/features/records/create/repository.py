from app.domain.entities.record import Record
from lib.repository.sa import BaseRepository


class RecordRepository(BaseRepository[Record]):
    """Repository class for `Record` model."""

    async def create_record(
        self,
        *,
        created_by_id: int,
        start,
        end,
    ) -> Record:
        """Create record."""
        record = Record(
            created_by_id=created_by_id,
            start=start,
            end=end,
        )
        await self.add(record, flush=True)
        return record
