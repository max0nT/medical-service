import pydantic


class ReserveRecordCommand(pydantic.BaseModel):
    """Command class for reserving record."""

    pk: int
    user_id: int
    user_email: str
