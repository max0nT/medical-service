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
)

from .. import permissions

router = fastapi.APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/sign-up/",
    response_model=entities.UserReadSchema,
    status_code=http.HTTPStatus.CREATED,
)
async def sign_up(
    data: entities.UserSignUpSchema,
    auth_client: typing.Annotated[
        protocols.AuthClientProtocol,
        fastapi.Depends(dependencies.get_auth_client),
    ],
) -> entities.UserReadSchema:
    """Sign up for clients."""
    async with settings.session_factory() as session:
        _, new_user = await auth_client.sign_up(session=session, data=data)
        await session.commit()
    return entities.UserReadSchema.model_validate(new_user).model_dump(
        mode="json",
    )


@router.post(
    "/login/",
    response_model=entities.AuthToken,
)
async def login(
    data: entities.UserSignInSchema,
    auth_client: typing.Annotated[
        protocols.AuthClientProtocol,
        fastapi.Depends(dependencies.get_auth_client),
    ],
) -> entities.AuthToken:
    """Sign in for client."""
    async with settings.session_factory() as session:
        token = await auth_client.authenticate(
            session=session,
            data=data,
        )
        await session.close()
    return entities.AuthToken(access_token=token)


@router.post(
    path="/logout/",
    status_code=http.HTTPStatus.NO_CONTENT,
)
async def logout(
    token: typing.Annotated[
        str,
        fastapi.Depends(dependencies.oauth2_scheme),
    ],
    auth_client: typing.Annotated[
        protocols.AuthClientProtocol,
        fastapi.Depends(dependencies.get_auth_client),
    ],
) -> fastapi.Response:
    """Do logout."""
    await auth_client.move_token_to_black_list(token=token)
    return fastapi.Response(status_code=http.HTTPStatus.NO_CONTENT)


@router.get(
    path="/me/",
    response_model=entities.UserReadSchema,
)
@permissions.permission_list(
    permission_classes=(permissions.IsAuthenticatedPermission,),
)
async def me(request: lib.Request) -> entities.UserReadSchema:
    """Get info about user by access token."""
    return entities.UserReadSchema.model_validate(request.user).model_dump(
        mode="json",
    )


@router.get("/")
@permissions.permission_list(
    permission_classes=(permissions.IsAuthenticatedPermission,),
)
async def select(
    request: lib.Request,
    user_repo: typing.Annotated[
        protocols.RepositoryProtocol[models.User],
        fastapi.Depends(dependencies.get_repo(models.User)),
    ],
) -> list[entities.UserReadSchema]:
    """Return list of `User` instances."""
    async with settings.session_factory() as session:
        result_list = await user_repo.select(session=session)
        await session.close()
    return [
        entities.UserReadSchema.model_validate(record)
        for record in result_list
    ]


@router.get("/{pk}/")
@permissions.permission_list(
    permission_classes=(permissions.IsAuthenticatedPermission,),
)
async def retrieve(
    request: lib.Request,
    user_repo: typing.Annotated[
        protocols.RepositoryProtocol[models.User],
        fastapi.Depends(dependencies.get_repo(models.User)),
    ],
    pk: int,
) -> entities.UserReadSchema:
    """Return one `User` instance by id."""
    async with settings.session_factory() as session:
        instance = await user_repo.select_one(session=session, pk=pk)
        await session.close()
    return entities.UserReadSchema.model_validate(instance)


@router.put("/{pk}/")
@permissions.permission_list(
    permission_classes=(permissions.IsAuthenticatedPermission,),
)
async def update(
    request: fastapi.Request,
    user_repo: typing.Annotated[
        protocols.RepositoryProtocol[models.User],
        fastapi.Depends(dependencies.get_repo(models.User)),
    ],
    pk: int,
    data: typing.Annotated[entities.UserWriteSchema, fastapi.Form()],
    # avatar: fastapi.UploadFile | None = None,
) -> entities.UserReadSchema:
    """Update `Record` instance."""
    async with settings.session_factory() as session:
        updated_instance = await user_repo.update(
            session=session,
            pk=pk,
            **data.model_dump(),
            # avatar=avatar,
        )
        await session.commit()
    return entities.UserReadSchema.model_validate(updated_instance)
