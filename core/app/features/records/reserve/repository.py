import sqlalchemy

from app.domain.entities.record import Record
from lib.repository.sa import BaseRepository


class RecordRepository(BaseRepository[Record]):
    """Repository class for `Record` model."""

    async def reserve_record(
        self,
        *,
        pk: int,
    ) -> Record:
        """Return record with users locked for reservation."""
        stmt = (
            sqlalchemy.select(Record)
            .where(Record.id == pk)
            .options(
                sqlalchemy.orm.joinedload(Record.created_by),
                sqlalchemy.orm.joinedload(Record.reserved_by),
            )
            .with_for_update()
        )
        raw_result = await self.session.execute(stmt)
        record = raw_result.scalar_one_or_none()
        if record is None:
            return await self.select_one(pk=pk)
        return record
