import logging
import signal
import threading
from concurrent import futures

import grpc
from dishka import make_container
from dishka.integrations.grpcio import DishkaInterceptor

from document_service.features.document_recognition.provider import (
    DocumentRecognitionProvider,
)
from document_service.features.document_recognition.service import (
    DocumentRecognitionService,
)
from document_service.infrastructure.config.config import (
    OllamaConfig,
    get_settings,
)
from document_service.infrastructure.grpc.compiled import document_pb2_grpc

LOGGER = logging.getLogger(__name__)
GRACEFUL_SHUTDOWN_TIMEOUT_SECONDS = 10


def build_server() -> tuple[grpc.Server, object]:
    settings = get_settings()
    container = make_container(
        DocumentRecognitionProvider(),
        context={OllamaConfig: settings.ollama},
    )
    grpc_server = grpc.server(
        thread_pool=futures.ThreadPoolExecutor(
            max_workers=settings.grpc.grpc_max_workers,
        ),
        interceptors=[DishkaInterceptor(container)],
    )
    document_pb2_grpc.add_DocumentRecognitionServiceServicer_to_server(
        DocumentRecognitionService(),
        grpc_server,
    )
    grpc_server.add_insecure_port(
        f"{settings.grpc.grpc_host}:{settings.grpc.grpc_port}",
    )
    return grpc_server, container


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = get_settings()
    grpc_server, container = build_server()
    stop_event = threading.Event()

    def _request_shutdown(signum: int, _: object) -> None:
        LOGGER.info("Received signal %s, starting graceful shutdown", signum)
        stop_event.set()

    signal.signal(signal.SIGINT, _request_shutdown)
    signal.signal(signal.SIGTERM, _request_shutdown)

    LOGGER.info(
        "Starting gRPC server on %s:%s",
        settings.grpc.grpc_host,
        settings.grpc.grpc_port,
    )
    grpc_server.start()
    LOGGER.info("gRPC server started")

    try:
        stop_event.wait()
    finally:
        LOGGER.info(
            "Stopping gRPC server with %ss grace period",
            GRACEFUL_SHUTDOWN_TIMEOUT_SECONDS,
        )
        grpc_server.stop(
            GRACEFUL_SHUTDOWN_TIMEOUT_SECONDS,
        ).wait(GRACEFUL_SHUTDOWN_TIMEOUT_SECONDS)
        container.close()
        LOGGER.info("Shutdown completed")


if __name__ == "__main__":
    main()
