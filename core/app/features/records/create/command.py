import datetime

import pydantic


class CreateRecordCommand(pydantic.BaseModel):
    """Command class for creating record."""

    created_by_id: int
    start: datetime.date
    end: datetime.date
