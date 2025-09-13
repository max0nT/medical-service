import http
import typing

import fastapi

from src import (
    dependencies,
    entities,
    extensions,
    permissions,
    repositories,
    services,
)

router = fastapi.APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/sign-up/",
    response_model=entities.UserReadSchema,
    status_code=http.HTTPStatus.CREATED,
)
async def sign_up(
    data: entities.UserSignUpSchema,
) -> entities.UserReadSchema:
    """Sign up for clients."""
    _, new_user = await services.AuthClient.create_auth_client().sign_up(
        data=data,
    )
    return entities.UserReadSchema.model_validate(new_user).model_dump(
        mode="json",
    )


@router.post(
    "/login/",
    response_model=entities.AuthToken,
)
async def login(
    data: entities.UserSignInSchema,
) -> entities.AuthToken:
    """Sign in for client."""
    token = await services.AuthClient.create_auth_client().authenticate(
        data=data,
    )
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
) -> fastapi.Response:
    """Do logout."""
    await services.AuthClient.create_auth_client().move_token_to_black_list(
        token=token,
    )
    return fastapi.Response(status_code=http.HTTPStatus.NO_CONTENT)


@router.get(
    path="/me/",
    response_model=entities.UserReadSchema,
)
@permissions.permission_list(
    permission_classes=(permissions.IsAuthenticatedPermission,),
)
async def me(request: extensions.Request) -> entities.UserReadSchema:
    """Get info about user by access token."""
    return entities.UserReadSchema.model_validate(request.user).model_dump(
        mode="json",
    )


@router.get("/")
@permissions.permission_list(
    permission_classes=(permissions.IsAuthenticatedPermission,),
)
async def get_list(
    request: extensions.Request,
) -> list[entities.UserReadSchema]:
    """Return list of `User` instances."""
    repository = await repositories.UserRepository.create_repository()
    result_list = await repository.get_list()
    return [
        entities.UserReadSchema.model_validate(record)
        for record in result_list
    ]


@router.get("/{pk}/")
@permissions.permission_list(
    permission_classes=(permissions.IsAuthenticatedPermission,),
)
async def retrieve(
    request: extensions.Request,
    pk: int,
) -> entities.UserReadSchema:
    """Return one `User` instance by id."""
    repository = await repositories.UserRepository.create_repository()
    instance = await repository.retrieve_one(pk=pk)
    if not instance:
        raise fastapi.HTTPException(status_code=http.HTTPStatus.NOT_FOUND)

    return entities.UserReadSchema.model_validate(instance)


@router.put("/{pk}/")
@permissions.permission_list(
    permission_classes=(permissions.IsAuthenticatedPermission,),
)
async def update(
    request: extensions.Request,
    pk: int,
    data: entities.UserWriteSchema,
) -> entities.UserReadSchema:
    """Update `Record` instance."""
    repository = await repositories.UserRepository.create_repository()
    instance = await repository.retrieve_one(pk=pk)
    if not instance:
        raise fastapi.HTTPException(status_code=http.HTTPStatus.NOT_FOUND)
    updated_instance = await repository.update_one(pk=pk, **data.model_dump())
    return entities.UserReadSchema.model_validate(updated_instance)
