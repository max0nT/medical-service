import grpc
from dishka.integrations.grpcio import FromDishka, inject

from document_service.features.document_recognition.dto import (
    DocumentRecognitionRequestDTO,
)
from document_service.features.document_recognition.handler import (
    DocumentRecognitionHandler,
)
from document_service.infrastructure.grpc.compiled import (
    document__pb2,
    document_pb2_grpc,
)


class DocumentRecognitionService(
    document_pb2_grpc.DocumentRecognitionServiceServicer,
):
    """Class for `DocumentRecognitionService` grpc server."""

    @inject
    def DocumentRecognition(
        self,
        request: document__pb2.DocumentRecognitionRequest,
        context: grpc.ServicerContext,
        handler: FromDishka[DocumentRecognitionHandler],
    ) -> document__pb2.DocumentRecognitionResponse:
        response_dto = handler(
            DocumentRecognitionRequestDTO(
                image_base64=request.image_base64,
            ),
        )
        return document__pb2.DocumentRecognitionResponse(raw=response_dto.raw)
