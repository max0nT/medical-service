import fastapi

from app.features.users.delete.router import router as delete_router
from app.features.users.list.router import router as list_router
from app.features.users.me.router import router as me_router
from app.features.users.update.router import router as update_router

users_router = fastapi.APIRouter()

users_router.include_router(me_router)
users_router.include_router(list_router)
users_router.include_router(update_router)
users_router.include_router(delete_router)
