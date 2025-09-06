import arrow
import httpx
import pytest
import pytest_lazy_fixtures

from src import entities, models, repositories
from src.entities.record import RecordWriteSchema

from .. import utils


@pytest.mark.parametrize(
    argnames=[
        "parametrized_user",
        "expected_status_code",
    ],
    argvalues=[
        (pytest_lazy_fixtures.lf("user"), httpx.codes.CREATED),
        (
            pytest_lazy_fixtures.lf("user_as_client"),
            httpx.codes.FORBIDDEN,
        ),
    ],
)
async def test_api(
    parametrized_user: models.User,
    expected_status_code: int,
) -> None:
    """Test record created works correctly."""
    api_client = utils.user_api_client(user=parametrized_user)
    request_data = RecordWriteSchema(
        start=arrow.utcnow().date(),
        end=arrow.utcnow().shift(hours=1).date(),
    )
    response: httpx.Response = await api_client.post(
        "/records/",
        content=request_data.model_dump_json(),
    )

    assert response.status_code == expected_status_code
    if not response.is_success:
        return

    response_data = entities.RecordReadSchema.model_validate_json(
        response.content,
    )
    repo = await repositories.RecordRepository.create_repository()

    instance = await repo.retrieve_one(pk=response_data.id)
    assert instance

    await repo.delete_one(pk=instance.id)
