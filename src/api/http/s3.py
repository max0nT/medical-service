import datetime

import fastapi

from src import entities
from src.lib import s3_backend

router = fastapi.APIRouter(
    prefix="/s3",
    tags=["s3"],
)


@router.post(
    path="/upload/",
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def upload_file(
    file: fastapi.UploadFile,
) -> entities.S3Path:
    """Upload image to s3."""
    s3_filename = s3_backend.write(
        file=file.file,
        name=f"photo{datetime.datetime.now().strftime('_%d_%m_%Y__%H_%M_%S')}",
    )
    return entities.S3Path(path=s3_backend.get_path(s3_filename))
