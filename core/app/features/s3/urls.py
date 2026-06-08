import fastapi

from app.features.s3.upload.router import router as upload_router

s3_router = fastapi.APIRouter()

s3_router.include_router(upload_router)
