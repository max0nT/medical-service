import http

import fastapi

from config import settings

from src import models, protocols


async def reserve(
    record_pk: int,
    record_repo: protocols.RepositoryProtocol[models.Record],
    user: models.User,
):
    """Implement reserve logic."""
    async with settings.session_factory() as session:
        record = await record_repo.select_one(session=session, pk=record_pk)
        if record.reserved_by_id and record.reserved_by_id != user.id:
            raise fastapi.HTTPException(
                status_code=http.HTTPStatus.BAD_REQUEST,
                detail={"detail": "Record was reserved"},
            )
        reserved_by_id = user.id if record.reserved_by_id else None
        updated_instance = await record_repo.update(
            session=session,
            pk=record.id,
            reserved_by_id=reserved_by_id,
        )
        await session.close()
    return updated_instance
