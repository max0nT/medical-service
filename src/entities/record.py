import datetime
import typing

import pydantic

from .core import BaseReadModelSchema


class RecordReadSchema(BaseReadModelSchema):
    """Describe `Record` schema for readable actions."""

    created_by_id: int | None
    reserved_by_id: int | None
    start: datetime.date
    end: datetime.date

    @pydantic.field_validator("start", "end", mode="before")
    @classmethod
    def get_date(cls, value: typing.Any):
        if not isinstance(value, datetime.datetime):
            return value
        return value.date()


class RecordWriteSchema(pydantic.BaseModel):
    """Describe `Record` schema for writable actions."""

    start: datetime.date
    end: datetime.date
