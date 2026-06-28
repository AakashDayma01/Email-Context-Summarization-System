from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings
import base64
import hashlib


def get_cipher():
    # Convert any key string into a valid Fernet key
    key = hashlib.sha256(settings.ENCRYPTION_KEY.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))


class EmailSummary(models.Model):
    client = models.OneToOneField("clients.Client", on_delete=models.CASCADE, related_name="summary",)
    encrypted_summary = models.TextField()
    emails_processed = models.PositiveIntegerField(default=0)
    last_refreshed = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "email_summaries"

    def __str__(self):
        return f"Summary - {self.client.name}"

    @property
    def decrypted_summary(self):
        cipher = get_cipher()
        return cipher.decrypt(self.encrypted_summary.encode()).decode()

    def set_summary(self, text):
        cipher = get_cipher()
        self.encrypted_summary = cipher.encrypt(text.encode()).decode()