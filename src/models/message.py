import sqlalchemy
import sqlalchemy.orm

from .core import BaseModel


class Message(BaseModel):
    """Class to keep messages."""

    __tablename__ = "message"

    content = sqlalchemy.Column(name="content", type_=sqlalchemy.Text())

    chat_id = sqlalchemy.Column(
        "chat_id",
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey("chat.id"),
    )
    user_id = sqlalchemy.Column(
        "user_id",
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey("users.id"),
    )

    chat = sqlalchemy.orm.relationship(
        argument="Chat",
        back_populates="chat",
    )
