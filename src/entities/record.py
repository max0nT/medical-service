import datetime

import pydantic

from .core import BaseReadModelSchema


class RecordReadSchema(BaseReadModelSchema):
    """Describe `Record` schema for readable actions."""

    created_by_id: int | None
    reserved_by_id: int | None
    start: datetime.date
    end: datetime.date


class RecordWriteSchema(pydantic.BaseModel):
    """Describe `Record` schema for writable actions."""

    start: datetime.date
    end: datetime.date
