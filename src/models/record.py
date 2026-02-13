import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.sql.schema import CheckConstraint

from .core import BaseModel, OnDelete


class Record(BaseModel):
    """Model describing info about slots created by employees."""

    __tablename__ = "record"

    created_by_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(
            column="users.id",
            ondelete=OnDelete.CASCADE.value,
        ),
        name="created_by_id",
    )
    reserved_by_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(
            column="users.id",
            ondelete=OnDelete.SET_NULL.value,
        ),
        name="reserved_by_id",
    )
    start = sqlalchemy.Column(
        name="start",
        type_=sqlalchemy.DateTime(),
    )
    end = sqlalchemy.Column(
        name="end",
        type_=sqlalchemy.DateTime(),
    )

    created_by = sqlalchemy.orm.relationship(
        argument="User",
        single_parent=True,
        foreign_keys=[created_by_id],
    )
    reserved_by = sqlalchemy.orm.relationship(
        argument="User",
        single_parent=True,
        foreign_keys=[reserved_by_id],
    )

    __tableargs__ = (CheckConstraint("created_by_id != reserved_by_id"),)

    @property
    def receiver_email(self) -> str:
        """Return receiver email."""
        return self.created_by.email

    @property
    def doctor_full_name(self) -> str:
        """Return doctor full name."""
        return f"{self.reserved_by.first_name} {self.reserved_by.last_name}"
