import datetime
import enum

import pydantic


class BaseModelSchema(pydantic.BaseModel):
    """Class to setup base config."""

    model_config = pydantic.ConfigDict(
        from_attributes=True,
    )


class EmailType(enum.StrEnum):
    SIGN_UP = "SIGN_UP"
    RECORD_IS_RESERVED = "RECORD_IS_RESERVED"


class BaseEmailNotification(BaseModelSchema):
    """Base class to describe data for email notifications."""

    email_type: EmailType


class BaseReadModelSchema(BaseModelSchema):
    """Define base schema to interact API with databse."""

    id: int
    created: datetime.datetime
    modified: datetime.datetime
