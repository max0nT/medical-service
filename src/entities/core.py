import datetime

import pydantic


class BaseReadModelSchema(pydantic.BaseModel):
    """Define base schema to interact API with databse."""

    model_config = pydantic.ConfigDict(
        from_attributes=True,
    )

    id: int
    created: datetime.datetime
    modified: datetime.datetime
