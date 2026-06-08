import fastapi

from lib.exceptions import ObjectNotFoundException


def handle_not_found(
    request: fastapi.Request,
    exc: ObjectNotFoundException,
) -> fastapi.Response:
    """Handle `ObjectNotFoundException`."""
    return fastapi.Response(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc),
        },
    )
