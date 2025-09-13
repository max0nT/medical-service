from email_notifications.grpc_config import email_pb2 as email__pb2

from src.grpc_clients.email_notifications import client as email_client


def send_email() -> None:
    """Send request to send email about something."""
    email_client.stub.SendEmail(
        email__pb2.Email(
            first_name="Some name",
            last_name="Some last name",
            type=email__pb2.Email.EmailType.SIGN_UP_SUCCESSFULLY,
        ),
    )
