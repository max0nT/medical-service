import dataclasses
import datetime

from app.domain.enums.user import Role


@dataclasses.dataclass
class User:
    id: int
    created: datetime.datetime
    modified: datetime.datetime
    email: str
    role: Role
    first_name: str | None
    last_name: str | None
    avatar: str | None
    password: str
    sync_with_google_calendar: bool
