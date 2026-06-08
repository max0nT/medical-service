import http

import fastapi

from dishka.integrations.fastapi import FromDishka, inject

from app.features.s3.upload.command import UploadS3FileCommand
from app.features.s3.upload.dto import S3PathDTO
from app.features.s3.upload.handler import UploadS3FileHandler

router = fastapi.APIRouter(
    prefix="/s3",
    tags=["s3"],
)


@router.post(
    path="/upload/",
    response_model=S3PathDTO,
    status_code=http.HTTPStatus.CREATED,
)
@inject
async def upload_file(
    handler: FromDishka[UploadS3FileHandler],
    file: fastapi.UploadFile,
) -> S3PathDTO:
    """Upload image to s3."""
    s3_filename = await handler(
        command=UploadS3FileCommand(
            file=file.file,
        ),
    )
    return S3PathDTO(name=s3_filename)
