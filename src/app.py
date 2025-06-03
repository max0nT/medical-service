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
    allow_origins=["*"],  # или укажи конкретный адрес клиента
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(fastapi.exceptions.RequestValidationError)
async def validation_exception_handler(
    request: fastapi.Request,
    exc: fastapi.exceptions.RequestValidationError,
):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.error(request, exc_str)
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    print(await request.json())
    return fastapi.responses.JSONResponse(
        content=content,
        status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
