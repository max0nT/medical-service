import sqlalchemy

from .core import BaseModel


class TokenBlackList(BaseModel):
    """Model to save list of banned tokens."""
    
    __tablename__ = "token_black_list"

    value = sqlalchemy.Column(
        name="value",
        type_=sqlalchemy.String(255),
    )
