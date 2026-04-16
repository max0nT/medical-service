from dishka import Provider, Scope, provide

from document_service.features.document_recognition.handler import (
    DocumentRecognitionHandler,
)


class DocumentRecognitionProvider(Provider):
    """Provider class for `DocumentRecognition` handler."""

    scope = Scope.REQUEST

    handler = provide(
        DocumentRecognitionHandler,
        scope=Scope.REQUEST,
    )
