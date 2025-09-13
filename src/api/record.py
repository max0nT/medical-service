import http

import fastapi

from src import (
    entities,
    extensions,
    permissions,
    repositories,
    services,
)
from src.models.record import Record

router = fastapi.APIRouter(prefix="/records", tags=["Records"])


@router.get("/")
@permissions.permission_list(
    permission_classes=(permissions.IsAuthenticatedPermission,),
)
async def get_list(
    request: extensions.Request,
    created_by: int | None = None,
    reserved_by: int | None = None,
) -> list[entities.RecordReadSchema]:
    """Return list of `Record` instances."""
    filters = {}
    if created_by:
        filters["created_by_id"] = created_by
    if reserved_by:
        filters["reserved_by"] = reserved_by

    repository = await repositories.RecordRepository.create_repository()
    result_list = await repository.get_list(
        **filters,
    )
    return [
        entities.RecordReadSchema.model_validate(record)
        for record in result_list
    ]


@router.get("/{pk}/")
@permissions.permission_list(
    permission_classes=(permissions.IsAuthenticatedPermission,),
)
async def retrieve(
    request: extensions.Request,
    pk: int,
) -> entities.RecordReadSchema:
    """Return one `Record` instance by id."""
    repository = await repositories.RecordRepository.create_repository()
    instance = await repository.retrieve_one(pk=pk, raise_error=True)
    return entities.RecordReadSchema.model_validate(instance)


@router.post("/", status_code=http.HTTPStatus.CREATED)
@permissions.permission_list(
    permission_classes=(
        permissions.IsAuthenticatedPermission,
        permissions.UserEmployeePermission,
    ),
)
async def create(
    request: extensions.Request,
    data: entities.RecordWriteSchema,
) -> entities.RecordReadSchema:
    """Create `Record` instance."""
    repository = await repositories.RecordRepository.create_repository()
    instance: Record = await repository.create_one(
        created_by_id=request.user.id,
        **data.model_dump(),
    )
    return entities.RecordReadSchema.model_validate(instance)


@router.put("/{pk}/")
@permissions.permission_list(
    permission_classes=(
        permissions.IsAuthenticatedPermission,
        permissions.UserEmployeePermission,
    ),
)
async def update(
    request: extensions.Request,
    pk: int,
    data: entities.RecordWriteSchema,
) -> entities.RecordReadSchema:
    """Update `Record` instance."""

    repository = await repositories.RecordRepository.create_repository()
    await repository.retrieve_one(pk=pk, raise_error=True)

    updated_instance = await repository.update_one(pk=pk, **data.model_dump())
    return entities.RecordReadSchema.model_validate(updated_instance)


@router.put("/reserve/{pk}/")
@permissions.permission_list(
    permission_classes=(
        permissions.IsAuthenticatedPermission,
        permissions.UserClientPermission,
    ),
)
async def reserve(
    request: extensions.Request,
    pk: int,
) -> entities.RecordReadSchema:
    repository = await repositories.RecordRepository.create_repository()
    instance = await repository.retrieve_one(pk=pk, raise_error=True)

    updated_instance = await services.reserve(
        user=request.user,
        record=instance,
    )

    return entities.RecordReadSchema.model_validate(updated_instance)


@router.delete("/{pk}/")
@permissions.permission_list(
    permission_classes=(
        permissions.IsAuthenticatedPermission,
        permissions.UserEmployeePermission,
    ),
)
async def delete(
    request: extensions.Request,
    pk: int,
) -> fastapi.Response:
    """Delete `Record` instance."""
    repository = await repositories.RecordRepository.create_repository()
    is_deleted = await repository.delete_one(pk=pk)
    if not is_deleted:
        raise fastapi.HTTPException(status_code=http.HTTPStatus.NOT_FOUND)
    return fastapi.Response(status_code=http.HTTPStatus.NO_CONTENT)
