import datetime

import pydantic


class BaseEmailBody(pydantic.BaseModel):
    """Base model for email notification service.

    Contains receiver email for smtp server.

    """

    model_config = pydantic.ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime.datetime: lambda value: value.strftime("%d.%m.%y %H:%M"),
        },
    )

    email: str = pydantic.Field(
        validation_alias=pydantic.AliasChoices(
            "email",
            "receiver_email",
        ),
    )


class EmailSignUpBody(BaseEmailBody):
    """Class to describe email data after sign up."""


class EmailReservedBody(BaseEmailBody):
    """Pydantic model for email service for record reserving."""

    reserved_at: datetime.datetime = pydantic.Field(
        validation_alias="start",
    )

    to: str = pydantic.Field(validation_alias="doctor_full_name")

    qr_code: str
