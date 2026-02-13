import http
import typing

import fastapi

from config import settings

from src import (
    dependencies,
    entities,
    lib,
    models,
    protocols,
    services,
)

from .. import permissions

router = fastapi.APIRouter(prefix="/records", tags=["Records"])


@router.get("/")
@permissions.permission_list(
    permission_classes=(permissions.IsAuthenticatedPermission,),
)
async def select(
    request: lib.Request,
    record_repo: typing.Annotated[
        protocols.RepositoryProtocol[models.Record],
        fastapi.Depends(dependencies.get_repo(models.Record)),
    ],
    created_by: int | None = None,
    reserved_by: int | None = None,
) -> list[entities.RecordReadSchema]:
    """Return list of `Record` instances."""
    filters = {}
    if created_by:
        filters["created_by_id"] = created_by
    if reserved_by:
        filters["reserved_by"] = reserved_by

    async with settings.session_factory() as session:
        result_list = await record_repo.select(
            session=session,
            **filters,
        )
        await session.close()

    return [
        entities.RecordReadSchema.model_validate(record)
        for record in result_list
    ]


@router.get("/{pk}/")
@permissions.permission_list(
    permission_classes=(permissions.IsAuthenticatedPermission,),
)
async def retrieve(
    request: lib.Request,
    record_repo: typing.Annotated[
        protocols.RepositoryProtocol[models.Record],
        fastapi.Depends(dependencies.get_repo(models.Record)),
    ],
    pk: int,
) -> entities.RecordReadSchema:
    """Return one `Record` instance by id."""
    async with settings.session_factory() as session:
        instance = await record_repo.select_one(session=session, pk=pk)
        await session.commit()
    return entities.RecordReadSchema.model_validate(instance)


@router.post("/", status_code=http.HTTPStatus.CREATED)
@permissions.permission_list(
    permission_classes=(
        permissions.IsAuthenticatedPermission,
        permissions.UserEmployeePermission,
    ),
)
async def create(
    request: lib.Request,
    record_repo: typing.Annotated[
        protocols.RepositoryProtocol[models.Record],
        fastapi.Depends(dependencies.get_repo(models.Record)),
    ],
    data: entities.RecordWriteSchema,
) -> entities.RecordReadSchema:
    """Create `Record` instance."""
    async with settings.session_factory() as session:
        instance: models.Record = await record_repo.insert(
            session=session,
            created_by_id=request.user.id,
            **data.model_dump(),
        )
        await session.commit()
    return entities.RecordReadSchema.model_validate(instance)


@router.put("/{pk}/")
@permissions.permission_list(
    permission_classes=(
        permissions.IsAuthenticatedPermission,
        permissions.UserEmployeePermission,
    ),
)
async def update(
    request: lib.Request,
    record_repo: typing.Annotated[
        protocols.RepositoryProtocol[models.Record],
        fastapi.Depends(dependencies.get_repo(models.Record)),
    ],
    pk: int,
    data: entities.RecordWriteSchema,
) -> entities.RecordReadSchema:
    """Update `Record` instance."""
    async with settings.session_factory() as session:
        updated_instance = await record_repo.update(
            session=session,
            pk=pk,
            **data.model_dump(),
        )
        await session.commit()

    return entities.RecordReadSchema.model_validate(updated_instance)


@router.put("/reserve/{pk}/")
@permissions.permission_list(
    permission_classes=(
        permissions.IsAuthenticatedPermission,
        permissions.UserClientPermission,
    ),
)
async def reserve(
    request: lib.Request,
    record_repo: typing.Annotated[
        protocols.RepositoryProtocol[models.Record],
        fastapi.Depends(dependencies.get_repo(models.Record)),
    ],
    qr_code_generator: typing.Annotated[
        services.QrCodeGenerator,
        fastapi.Depends(services.get_qr_code_generator),
    ],
    pk: int,
) -> entities.RecordReadSchema:
    updated_instance = await services.reserve(
        record_repo=record_repo,
        record_pk=pk,
        user=request.user,
        qr_code_generator=qr_code_generator,
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
    request: lib.Request,
    record_repo: typing.Annotated[
        protocols.RepositoryProtocol[models.Record],
        fastapi.Depends(dependencies.get_repo(models.Record)),
    ],
    pk: int,
) -> fastapi.Response:
    """Delete `Record` instance."""
    async with settings.session_factory() as session:
        is_deleted = await record_repo.delete(session=session, pk=pk)
        await session.commit()
    if not is_deleted:
        raise fastapi.HTTPException(status_code=http.HTTPStatus.NOT_FOUND)
    return fastapi.Response(status_code=http.HTTPStatus.NO_CONTENT)
