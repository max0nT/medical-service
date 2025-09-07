import grpc

from . import email_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = email_pb2_grpc.EmailSendStub(channel)
