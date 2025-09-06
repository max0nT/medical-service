import factory

from config import settings

from src import models

from .base import BaseFactory


class RecordFactory(BaseFactory):
    """Factory class for `Record` model."""

    created_by = factory.SubFactory(
        "src.factories.user.UserFactory",
        role=models.User.Role.admin,
    )
    reserved_by = factory.SubFactory(
        "src.factories.user.UserFactory",
        role=models.User.Role.client,
    )
    start = factory.Faker("date_time_ad")
    end = factory.Faker("date_time_ad")

    class Meta:
        model = models.Record
        sqlalchemy_session_factory = settings.session_factory
