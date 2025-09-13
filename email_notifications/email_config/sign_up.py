import pathlib

from jinja2 import Template

from .base import BaseEmailNotification


class SignUpNotification(BaseEmailNotification):
    """Notification for sign up message."""

    subject = "You've signed up to our app"
    template = "email_notifications/templates/sign_up.html"

    def __init__(
        self,
        email: str,
        first_name: str,
        last_name: str,
    ):
        super().__init__(email=email)
        self.first_name = first_name
        self.last_name = last_name

    @property
    def content(self) -> str:
        raw_content = pathlib.Path(self.template).read_text()
        template = Template(raw_content)
        return template.render(
            email=self.email_to,
            full_name=self.full_name,
        )

    @property
    def full_name(self) -> str:
        return (
            f"{self.first_name} {self.last_name}"
            if self.first_name and self.last_name
            else self.email_to
        )
