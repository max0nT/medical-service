from sqladmin import ModelView

from src.models import User


class UserAdmin(ModelView, model=User):
    """Admin UI fro `User` model."""

    column_list = (
        User.id,
        User.created,
        User.modified,
        User.email,
        User.first_name,
        User.last_name,
        User.role,
        User.avatar,
    )
