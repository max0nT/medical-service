import fastapi

from app.features.records.create.router import router as create_router
from app.features.records.delete.router import router as delete_router
from app.features.records.list.router import router as list_router
from app.features.records.reserve.router import router as reserve_router
from app.features.records.retrieve.router import router as retrieve_router
from app.features.records.update.router import router as update_router

records_router = fastapi.APIRouter()

records_router.include_router(list_router)
records_router.include_router(create_router)
records_router.include_router(update_router)
records_router.include_router(reserve_router)
records_router.include_router(retrieve_router)
records_router.include_router(delete_router)
