import http

import fastapi

from src import models


def user_is_employee(user: models.User) -> None:
    """Check if user isn't employee raise 403 error."""
    if user.role != models.User.Role.employee:
        raise fastapi.HTTPException(
            status_code=http.HTTPStatus.FORBIDDEN,
            detail={"detail": "User isn't empoyee to performa that action."},
        )
