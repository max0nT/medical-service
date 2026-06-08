import pydantic


class DeleteUserCommand(pydantic.BaseModel):
    """Command class for deleting user."""

    pk: int
    current_user_id: int
