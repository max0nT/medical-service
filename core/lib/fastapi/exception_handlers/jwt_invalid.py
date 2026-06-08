import fastapi

from jwt.exceptions import InvalidTokenError


def handle_jwt_invalid(
    request: fastapi.Request,
    exc: InvalidTokenError,
) -> fastapi.Response:
    """Handler jwt invalid."""
    return fastapi.Response(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        content={
            "detail": "Jwt token is invalid or expired",
        },
    )
