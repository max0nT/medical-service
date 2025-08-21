import logging

import fastapi
import fastapi.middleware
import fastapi.middleware.cors

from src import api

app = fastapi.FastAPI()
app.include_router(api.record_api_router)
app.include_router(api.user_api_router)
app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
