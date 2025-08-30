import datetime

import pydantic


class BaseModelSchema(pydantic.BaseModel):
    """Class to setup base config."""

    model_config = pydantic.ConfigDict(
        from_attributes=True,
    )


class BaseReadModelSchema(BaseModelSchema):
    """Define base schema to interact API with databse."""

    id: int
    created: datetime.datetime
    modified: datetime.datetime
