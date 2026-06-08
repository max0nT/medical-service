import fastapi

from dishka.integrations.fastapi import FromDishka, inject

from app.features.auth.sign_up.command import SignUpCommand
from app.features.auth.sign_up.dto import SignUpDTO, SignUpResponseDTO
from app.features.auth.sign_up.handler import SignUpHandler

router = fastapi.APIRouter(tags=["Users"])


@router.post(
    "/users/sign-up/",
)
@inject
async def sign_up(
    data: SignUpDTO,
    handler: FromDishka[SignUpHandler],
) -> SignUpResponseDTO:
    """Sign up for clients."""
    user = await handler(
        command=SignUpCommand(
            email=data.email,
            password=data.password,
            password_repeat=data.password_repeat,
        ),
    )
    return SignUpResponseDTO.model_validate(user)
