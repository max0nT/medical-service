import grpc

from email_notifications.grpc_config import email_pb2_grpc

channel = grpc.insecure_channel("localhost:50051")
stub = email_pb2_grpc.EmailSendStub(channel)
