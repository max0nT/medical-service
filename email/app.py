import concurrent.futures as futures

import grpc
from grpc_schemes import email_pb2

from src.grpc.email import email_pb2_grpc as email_grpc


class EmailNotification(email_grpc.EmailSendServicer):
    """Email notification class."""

    def SendEmail(self, request, context):
        print("Stub to ensure grpc works")
        return email_pb2.Response(status_code=204)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    email_grpc.add_EmailSendServicer_to_server(
        servicer=EmailNotification()
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
