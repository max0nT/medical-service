from app.domain.entities.record import Record
from lib.repository.sa import BaseRepository


class RecordRepository(BaseRepository[Record]):
    """Repository class for `Record` model."""

    async def delete_record(
        self,
        *,
        pk: int,
    ) -> None:
        """Delete record by primary key."""
        record = await self.select_one(pk=pk)
        await self.delete(instance=record)
