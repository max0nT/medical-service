import sqlalchemy
import sqlalchemy.orm

from .core import BaseModel


class SecondaryChatUser(BaseModel):
    """Model to make m2m relation between user and chat models."""

    __tablename__ = "secondary_chat_user"

    user_id = sqlalchemy.Column(
        "user_id",
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey("users.id"),
    )
    chat_id = sqlalchemy.Column(
        "chat_id",
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey("chat.id"),
    )

    user = sqlalchemy.orm.relationship(
        argument="User",
        foreign_keys=[user_id],
    )
    chat = sqlalchemy.orm.relationship(
        argument="Chat",
        foreign_keys=[chat_id],
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint(
            "user_id",
            "chat_id",
            name="unique_user_chat",
        ),
    )


class Chat(BaseModel):
    """Model to describe chat for keep messages for user conversation."""

    __tablename__ = "chat"

    messages = sqlalchemy.orm.relationship(
        argument="Message",
        back_populates="chat",
    )

    users = sqlalchemy.orm.relationship(
        argument="User",
        secondary=SecondaryChatUser,
    )
