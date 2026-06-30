from django.conf import settings
from django.db import models


class Email(models.Model):
    """
    Represents an email exchanged with a client.

    Every email belongs to a client and is managed by an accountant.
    These emails are used to generate AI-powered contextual summaries.
    """

    # Client to whom the email belongs
    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.CASCADE,
        related_name="emails",
    )

    # Accountant responsible for this email
    accountant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="emails",
        limit_choices_to={"role": "ACCOUNTANT"},
    )

    subject = models.CharField(max_length=255)

    body = models.TextField()

    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "emails"
        ordering = ["-sent_at"]

    def __str__(self):
        return f"{self.client.name} - {self.subject}"