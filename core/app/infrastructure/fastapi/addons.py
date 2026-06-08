import fastapi

from scalar_fastapi import get_scalar_api_reference

router = fastapi.APIRouter()


@router.get("/", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference()
