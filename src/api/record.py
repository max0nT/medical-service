import http
import typing

import fastapi

from src import (
    dependencies,
    entities,
    models,
    permissions,
    repositories,
    services,
)
from src.models.record import Record

router = fastapi.APIRouter(prefix="/records", tags=["Records"])


@router.get("/")
async def get_list(
    user: typing.Annotated[
        models.User,
        fastapi.Depends(dependencies.auth_user),
    ],
    created_by: int | None = None,
    reserved_by: int | None = None,
) -> list[entities.RecordReadSchema]:
    """Retrun list of `Record` instances."""
    filters = {}
    if created_by:
        filters["created_by_id"] = created_by
    if reserved_by:
        filters["reserved_by"] = reserved_by

    repository = await repositories.RecordRepository.create_repository()
    result_list = await repository.get_list(
        **filters,
    )
    return [entities.RecordReadSchema.model_validate(record) for record in result_list]


@router.get("/{pk}/")
async def retrieve(
    user: typing.Annotated[
        models.User,
        fastapi.Depends(dependencies.auth_user),
    ],
    pk: int,
) -> entities.RecordReadSchema:
    """Retrun one `Record` instance by id."""
    repository = await repositories.RecordRepository.create_repository()
    instance = await repository.retrieve_one(pk=pk)
    if not instance:
        raise fastapi.HTTPException(status_code=http.HTTPStatus.NOT_FOUND)

    return entities.RecordReadSchema.model_validate(instance)


@router.post("/")
async def create(
    user: typing.Annotated[
        models.User,
        fastapi.Depends(dependencies.auth_user),
    ],
    data: entities.RecordWriteSchema,
) -> entities.RecordReadSchema:
    """Create `Record` instance."""
    permissions.user_is_employee(user=user)
    repository = await repositories.RecordRepository.create_repository()
    instance: Record = await repository.create_one(
        crerated_by_id=user.id,
        **data.model_dump(mode="json"),
    )
    return entities.RecordReadSchema.model_validate(instance)


@router.put("{pk}/")
async def update(
    user: typing.Annotated[
        models.User,
        fastapi.Depends(dependencies.auth_user),
    ],
    pk: int,
    data: entities.RecordWriteSchema,
) -> entities.RecordReadSchema:
    """Update `Record` instance."""
    permissions.user_is_employee(user=user)

    repository = await repositories.RecordRepository.create_repository()
    instance = await repository.retrieve_one(pk=pk)
    if not instance:
        raise fastapi.HTTPException(status_code=http.HTTPStatus.NOT_FOUND)

    await repository.reconnect()
    updated_instance = await repository.update_one(pk=pk, **data.model_dump())
    return entities.RecordReadSchema.model_validate(updated_instance)


@router.put("/reserve/{pk}/")
async def reserve(
    user: typing.Annotated[
        models.User,
        fastapi.Depends(dependencies.auth_user),
    ],
    pk: int,
) -> entities.RecordReadSchema:
    permissions.user_is_client(user=user)
    repository = await repositories.RecordRepository.create_repository()
    instance = await repository.retrieve_one(pk=pk)
    if not instance:
        raise fastapi.HTTPException(status_code=http.HTTPStatus.NOT_FOUND)

    updated_instance = await services.reserve(
        user=user,
        record=instance,
    )
    return entities.RecordReadSchema.model_validate(updated_instance)


@router.delete("{pk}/")
async def delete(
    user: typing.Annotated[
        models.User,
        fastapi.Depends(dependencies.auth_user),
    ],
    pk: int,
) -> fastapi.Response:
    """Delete `Record` instance."""
    permissions.user_is_employee(user=user)
    repository = await repositories.RecordRepository.create_repository()
    is_deleted = await repository.delete_one(pk=pk)
    if not is_deleted:
        raise fastapi.HTTPException(status_code=http.HTTPStatus.NOT_FOUND)
    return fastapi.Response(status_code=http.HTTPStatus.NO_CONTENT)
