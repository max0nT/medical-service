import uuid

import factory
import factory.fuzzy

from config import settings

from src import models, services

from .base import BaseFactory

USER_PASSWORD = "New_Password"


class UserFactory(BaseFactory):
    """Factory class for `User` model."""

    email = factory.LazyAttribute(lambda _: str(uuid.uuid4()) + "@gmail.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    role = factory.fuzzy.FuzzyChoice(
        choices=[role.value for role in models.User.Role],
    )
    password = factory.LazyAttribute(
        lambda _: (
            services.AuthClient.hash_password(
                USER_PASSWORD,
            )
        ),
    )

    class Meta:
        model = models.User
        sqlalchemy_session_factory = settings.session_factory
