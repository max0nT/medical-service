import httpx
import pytest

from src import factories, models, repositories

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
    repo = await repositories.RecordRepository.create_repository()
    await repo.delete_one(pk=record.id)
