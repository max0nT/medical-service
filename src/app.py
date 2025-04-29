import fastapi

from src import api

app = fastapi.FastAPI()
app.include_router(api.record_api_router)
app.include_router(api.user_api_router)
