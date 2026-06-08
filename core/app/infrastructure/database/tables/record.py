import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.sql.schema import CheckConstraint

from app.domain.entities.record import Record
from app.infrastructure.database.tables import (
    BaseModel,
    OnDelete,
    mapper_registry,
)


class RecordTable(BaseModel):
    """Record table."""

    __tablename__ = "record"
    __table_args__ = (
        CheckConstraint("created_by_id != reserved_by_id"),
        {"keep_existing": True},
    )

    created_by_id = sqlalchemy.Column(
        "created_by_id",
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(
            column="users.id",
            ondelete=OnDelete.CASCADE.value,
        ),
        nullable=False,
    )
    reserved_by_id = sqlalchemy.Column(
        "reserved_by_id",
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(
            column="users.id",
            ondelete=OnDelete.SET_NULL.value,
        ),
        nullable=True,
    )
    start = sqlalchemy.Column(
        name="start",
        type_=sqlalchemy.DateTime(),
        nullable=False,
    )
    end = sqlalchemy.Column(
        name="end",
        type_=sqlalchemy.DateTime(),
        nullable=False,
    )


mapper_registry.map_imperatively(
    Record,
    RecordTable.__table__,
    properties={
        "created_by": sqlalchemy.orm.relationship(
            "User",
            single_parent=True,
            foreign_keys=[RecordTable.created_by_id],
        ),
        "reserved_by": sqlalchemy.orm.relationship(
            "User",
            single_parent=True,
            foreign_keys=[RecordTable.reserved_by_id],
        ),
    },
)
