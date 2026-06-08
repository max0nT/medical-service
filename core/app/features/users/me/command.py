import pydantic

from app.domain.entities.user import User


class GetMeCommand(pydantic.BaseModel):
    """Command class for getting current user info."""

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    user: User
