import fastapi
import fastapi.encoders

import pydantic


class Checker:
    def __init__(self, model: pydantic.BaseModel):
        self.model = model

    def __call__(self, data: str = fastapi.Form(...)):
        try:
            return self.model.model_validate_json(data)
        except pydantic.ValidationError as e:
            raise fastapi.HTTPException(
                detail=fastapi.encoders.jsonable_encoder(e.errors()),
                status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
