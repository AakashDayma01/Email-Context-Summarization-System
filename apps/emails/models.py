from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models


class Email(models.Model):

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