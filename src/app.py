import fastapi
import fastapi.middleware
import fastapi.middleware.cors

import sqladmin
from scalar_fastapi import get_scalar_api_reference

from config import settings

from src import admin
from src.api import http as http_routers
from src.api import middleware
from src.api import ws as ws_routers

app = fastapi.FastAPI(redirect_slashes=False)
# Routers settings
app.include_router(http_routers.record_api_router)
app.include_router(http_routers.user_api_router)
app.include_router(ws_routers.ws_message_router)
# Middleware settings
app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(middleware.authorize)


@app.get("/", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        # Your OpenAPI document
        openapi_url=app.openapi_url,
        # Avoid CORS issues (optional)
        scalar_proxy_url="https://proxy.scalar.com",
    )


# Admin UI settings
Admin = sqladmin.Admin(app=app, engine=settings.engine)

Admin.add_view(admin.UserAdmin)
