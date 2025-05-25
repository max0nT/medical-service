import sqlalchemy
from sqlalchemy.sql.schema import CheckConstraint

from .core import BaseModel


class Record(BaseModel):
    """Model describing info about slots created by employees."""

    __tablename__ = "record"
    crerated_by_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(column="users.id"),
        name="created_by_id",
    )
    reserved_by_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(column="users.id"),
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

    __tableargs__ = (CheckConstraint("crerated_by_id != reserved_by_id"),)
