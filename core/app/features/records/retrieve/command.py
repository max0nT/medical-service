import pydantic


class RetrieveRecordCommand(pydantic.BaseModel):
    """Command class for retrieving record."""

    pk: int
