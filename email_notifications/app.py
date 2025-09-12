import concurrent.futures as futures
import logging

import grpc
from grpc_config import email_pb2 as email__pb2
from grpc_config import email_pb2_grpc

logger = logging.getLogger(__name__)


class EmailNotification(email_pb2_grpc.EmailSendServicer):
    """Email notification class."""

    def SendEmail(self, request, context):
        print("Stub to ensure grpc works")
        return email__pb2.Response(status_code=204)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    email_pb2_grpc.add_EmailSendServicer_to_server(
        servicer=EmailNotification(),
        server=server,
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    logger.info(
        "The grpc service have started successfully",
    )
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
