import uuid

import factory
import factory.fuzzy

from .base import BaseFactory

from src import models
from config import database


class UserFactory(BaseFactory):
    """Factory class for `User` model."""

    email = factory.LazyAttribute(
        lambda _: str(uuid.uuid4()) + "@gmail.com"
    )
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    role = factory.fuzzy.FuzzyChoice(
        choices=[
            role.value
            for role in models.User.Role
        ],
    )

    class Meta:
        model = models.User
        sqlalchemy_session_factory = database.session_factory
