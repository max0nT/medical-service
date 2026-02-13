import typing
import unittest
import unittest.mock

import httpx
import pytest

from config import settings

from src import factories, models

from . import utils

TEST_QR_CODE_IN_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAIQAAACEAQMAAABrihHkAAAABlBMVEX//"
    "/8AAABVwtN&#43;AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAy0lEQVRIie2U"
    "wQ3EMAgE6YD&#43;u6QDjiH2Kfe5yOw3CCUwD8usAbPXHiwzwy08CAQSOFkHAqk"
    "Y70AknisQSRXqoZJyN8i99nPSYmE/b3FOmsYtGZLKyr1aYV1wSKpIg&#43;S30hlx"
    "iqwkbF9zSPASnq8JBN35WoLnhK4k7rkTSDVleiY0FVKKcS6vuGsfEYR35jbTFNKqlep9"
    "ukAYkOzJDVcIDVmis972nWfkWmvcb588Jo5kvhaSQMhafoVcjxi0uAmkN5vzs9tbnJ"
    "PX/tgHtBMAsgb78UMAAAAASUVORK5CYII="
)


@pytest.fixture(autouse=True)
def mock_qr_generator() -> None:
    """Mocker qr api generator execution."""
    unittest.mock.patch(
        "src.services.qr_code.QRCodeClient.get_qr_code",
        lambda: TEST_QR_CODE_IN_BASE64,
    )


@pytest.fixture(scope="session")
async def user() -> typing.AsyncGenerator[models.User, None]:
    """Return employee User instance."""
    user = await factories.UserFactory(
        role=models.User.Role.employee,
    )
    yield user
    async with settings.session_factory() as session:
        await session.delete(user)
        await session.commit()


@pytest.fixture(scope="session")
async def user_as_client() -> typing.AsyncGenerator[models.User, None]:
    """Return client User instance."""
    yield (
        user := await factories.UserFactory(
            role=models.User.Role.client,
        )
    )
    async with settings.session_factory() as session:
        await session.delete(user)
        await session.commit()


@pytest.fixture(scope="session")
async def record() -> typing.AsyncGenerator[models.Record, None]:
    """Return Record instance."""
    record = await factories.RecordFactory.create()
    yield await record.joined_load("*")
    async with settings.session_factory() as session:
        await session.delete(record)
        await session.commit()


@pytest.fixture(scope="session")
def client() -> httpx.AsyncClient:
    """Init http client for tests."""
    return utils.client_factory()


@pytest.fixture(scope="session")
async def authorized_api_client(
    user: models.User,
) -> httpx.AsyncClient:
    """Return authorized api client."""
    return utils.user_api_client(user=user)
