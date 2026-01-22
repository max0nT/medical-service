import typing

import fastapi
import fastapi.middleware
import fastapi.middleware.cors

import sqladmin

from config import settings

from src import admin, api, dependencies, extensions, models

app = fastapi.FastAPI(redirect_slashes=False)
app.include_router(api.record_api_router)
app.include_router(api.user_api_router)
app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Admin = sqladmin.Admin(app=app, engine=settings.engine)

Admin.add_view(admin.UserAdmin)


@app.middleware("http")
async def authorize(
    request: fastapi.Request,
    next_call: typing.Callable,
) -> fastapi.Response:
    """Authenticate user vie bearer token."""
    user = None
    if "authorization" in request.headers:
        auth_client = dependencies.get_auth_client()

        token = await dependencies.oauth2_scheme(request=request)
        user_id = await auth_client.check_token_is_valid(
            token=token,
        )
        async with settings.session_factory() as session:
            user_repo = dependencies.get_repo(modelClass=models.User)()
            user: models.User | None = await user_repo.select_one(
                session=session,
                pk=user_id,
            )
            await session.close()

    request = extensions.Request(user=user, **request.__dict__)
    response = await next_call(request)
    return response
