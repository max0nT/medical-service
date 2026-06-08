import fastapi

from app.features.auth.login.router import router as login_router
from app.features.auth.logout.router import router as logout_router
from app.features.auth.sign_up.router import router as sign_up_router

auth_router = fastapi.APIRouter()

auth_router.include_router(sign_up_router)
auth_router.include_router(login_router)
auth_router.include_router(logout_router)
