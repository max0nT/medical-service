import pydantic


class ListRecordsCommand(pydantic.BaseModel):
    """Command class for listing records."""

    created_by: int | None = None
    reserved_by: int | None = None
