import http

import fastapi

from src import models, repositories


async def reserve(user: models.User, record: models.Record):
    """Implement reserve logic."""
    if record.reserved_by_id and record.reserved_by_id != user.id:
        raise fastapi.HTTPException(
            status_code=http.HTTPStatus.BAD_REQUEST,
            detail={"detail": "Record was reserved"},
        )
    reserved_by_id = user.id if record.reserved_by_id else None
    repository = await repositories.RecordRepository.create_repository()
    updated_instance = await repository.update_one(
        pk=record.id,
        reserved_by_id=reserved_by_id,
    )
    return updated_instance
