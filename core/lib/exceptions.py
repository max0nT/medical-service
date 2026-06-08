from typing import final


@final
class UnsolvableAnnotationsError(Exception):
    """
    Raised when we can't solve function's annotations using ``get_type_hints``.

    Only raised when there are no other options.
    """


class ObjectNotFoundException(Exception):
    """Exception to raise error when entry not found."""


class JwtInvalidException(Exception):
    """Exception to raise error when jwt token is invalid."""
