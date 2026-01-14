from .core import BaseEmailNotification, EmailType


class EmailSignUp(BaseEmailNotification):
    """Class to describe email data after sign up."""

    # Meta data
    email_type: EmailType = EmailType.SIGN_UP

    # Payload data
    email: str
