import fastapi
from fastapi.security import HTTPBearer

import uvicorn
from dishka.integrations.fastapi import setup_dishka

from app.features.auth.urls import auth_router
from app.features.records.urls import records_router
from app.features.s3.urls import s3_router
from app.features.users.urls import users_router
from app.infrastructure.fastapi.addons import router as addons_router
from app.infrastructure.fastapi.ioc import container
from lib.fastapi.exception_handlers.jwt_invalid import (
    InvalidTokenError,
    handle_jwt_invalid,
)
from lib.fastapi.exception_handlers.not_found import (
    ObjectNotFoundException,
    handle_not_found,
)
from lib.fastapi.middleware.authorize import authorize

app = fastapi.FastAPI(
    redirect_slashes=False,
    dependencies=[
        fastapi.Depends(HTTPBearer(auto_error=False)),
    ],
)
setup_dishka(container=container, app=app)

app.add_exception_handler(InvalidTokenError, handle_jwt_invalid)
app.add_exception_handler(ObjectNotFoundException, handle_not_found)

app.include_router(addons_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(records_router)
app.include_router(s3_router)
app.middleware("http")(authorize)

if __name__ == "__main__":
    uvicorn.run(
        "app.infrastructure.fastapi.app:app",
        reload=True,
        workers=1,
    )
