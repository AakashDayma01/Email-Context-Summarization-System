from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models


class Email(models.Model):
    """
    Represents an email associated with a client.

    Each email is linked to a client and the accountant who created
    or manages it. Email records are used as the primary input for
    generating AI-powered contextual summaries.
    """

    client = models.ForeignKey("clients.Client", on_delete=models.CASCADE, related_name="emails",)
    accountant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="emails",)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "emails"
        ordering = ["sent_at"]

    def __str__(self):
        return self.subject