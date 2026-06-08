import pydantic


class DeleteRecordCommand(pydantic.BaseModel):
    """Command class for deleting record."""

    pk: int
