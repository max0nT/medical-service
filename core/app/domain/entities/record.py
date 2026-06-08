import dataclasses
import datetime

from app.domain.entities.user import User


@dataclasses.dataclass
class Record:
    """Record entity."""

    id: int
    created: datetime.datetime
    modified: datetime.datetime
    created_by_id: int
    reserved_by_id: int | None
    start: datetime.datetime
    end: datetime.datetime
    created_by: User
    reserved_by: User | None

    @property
    def receiver_email(self) -> str:
        """Return receiver email."""
        return self.created_by.email

    @property
    def doctor_full_name(self) -> str:
        """Return doctor full name."""
        if self.reserved_by is None:
            return ""
        return f"{self.reserved_by.first_name} {self.reserved_by.last_name}"
