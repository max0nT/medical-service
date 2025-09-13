from email_notifications.grpc_config import email_pb2 as email__pb2

from src.grpc_clients.email_notifications import client as email_client


def send_sign_up_email(
    email: str,
    first_name: str,
    last_name: str,
) -> None:
    """Send request to send email about something."""
    email_client.stub.SendEmail(
        email__pb2.Email(
            email=email,
            first_name=first_name,
            last_name=last_name,
            type=email__pb2.Email.EmailType.SIGN_UP_SUCCESSFULLY,
        ),
    )
