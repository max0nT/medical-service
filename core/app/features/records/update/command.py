import datetime

import pydantic


class UpdateRecordCommand(pydantic.BaseModel):
    """Command class for updating record."""

    pk: int
    start: datetime.date
    end: datetime.date
