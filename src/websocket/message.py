import fastapi

import pydantic

from src import repositories as repos

router = fastapi.APIRouter(prefix="ws/")


class MessageData(pydantic.BaseModel):
    """Base class to describe data"""

    user_id: int
    content: str


@router.websocket("/chat/{chat_id}/")
async def message(
    websocket: fastapi.WebSocket,
    chat_id: int,
):
    """Send websocket message."""
    await websocket.accept()
    while True:
        raw_data = await websocket.receive_bytes()

        try:
            structured_data = MessageData.model_validate(
                raw_data.decode("utf-8"),
            )
        except pydantic.ValidationError as errors:
            error_dict = errors.errors()
            websocket.send_json(error_dict)
            continue

        chat_repo = await repos.ChatRepository.create_repository()
        msg_repo = await repos.MessageRepository.create_repository()

        chat = await chat_repo.retrieve_one(chat_id)
        if not chat:
            await websocket.send_json(
                {
                    "Error": "Chat not found",
                },
            )

        await msg_repo.create_one(
            **structured_data.model_dump(),
            chat_id=chat_id,
        )

        await websocket.send_json(structured_data.model_dump())
