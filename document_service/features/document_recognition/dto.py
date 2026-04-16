import pydantic


class DocumentRecognitionRequestDTO(pydantic.BaseModel):
    """DTO class for document recognition request."""

    image_base64: str


class DocumentRecognitionResponseDTO(pydantic.BaseModel):
    """DTO class for document recognition response."""

    raw: str
