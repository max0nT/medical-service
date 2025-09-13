import smtplib
from abc import abstractmethod
from email.message import EmailMessage


class BaseEmailNotification:
    """Base Notification class for email sending."""

    template: str
    subject: str

    def __init__(self, email: str) -> None:
        self.email_to = email

    @property
    @abstractmethod
    def content(self) -> str:
        """Get content for email sending."""

    def get_message(self) -> EmailMessage:
        email_message = EmailMessage()
        email_message["Subject"] = self.subject
        email_message["From"] = "medical.service@gmail.com"
        email_message["To"] = self.email_to
        email_message.set_content(self.content)
        return email_message

    def send(self) -> None:
        """Send email message."""
        message = self.get_message()
        with smtplib.SMTP(host="0.0.0.0", port=1025) as server:
            server.sendmail(
                "medical.service@gmail.com",
                self.email_to,
                message.as_string(),
            )
