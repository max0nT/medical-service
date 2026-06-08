import datetime
import typing

import pydantic


class RecordReadDTO(pydantic.BaseModel):
    """DTO class to represent record info."""

    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    created: datetime.datetime
    modified: datetime.datetime
    created_by_id: int | None
    reserved_by_id: int | None
    start: datetime.date
    end: datetime.date

    @pydantic.field_validator("start", "end", mode="before")
    @classmethod
    def get_date(cls, value: typing.Any):
        """Convert datetime values to date."""
        if not isinstance(value, datetime.datetime):
            return value
        return value.date()


class RecordWriteDTO(pydantic.BaseModel):
    """DTO class for writable record data."""

    start: datetime.date
    end: datetime.date
