import httpx
import pytest

from config import settings

from src import dependencies, factories, models

from .. import utils


@pytest.mark.parametrize(
    argnames=[
        "by_employee",
        "expected_status_code",
    ],
    argvalues=[
        (
            True,
            httpx.codes.FORBIDDEN,
        ),
        (
            False,
            httpx.codes.OK,
        ),
    ],
)
async def test_api(
    by_employee: bool,
    expected_status_code: int,
) -> None:
    """Test record reservation works correctly."""
    record: models.Record = await factories.RecordFactory()
    record = await record.joined_load("*")
    user = record.created_by if by_employee else record.reserved_by
    api_client = utils.user_api_client(user=user)

    response: httpx.Response = await api_client.put(
        f"/records/reserve/{record.id}/",
    )

    assert response.status_code == expected_status_code

    # Post clear
    repo = dependencies.get_repo(modelClass=models.Record)()
    session = settings.session_factory()
    await repo.delete(session=session, pk=record.id)
    await session.commit()
    await session.close()
