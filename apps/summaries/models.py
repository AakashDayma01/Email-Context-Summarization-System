from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings
import base64
import hashlib


def get_cipher():
    """
    Create and return a Fernet cipher instance.

    The encryption key defined in the project settings is converted
    into a valid Fernet-compatible key using SHA-256 hashing and
    Base64 URL-safe encoding.

    Returns:
        Fernet: Configured Fernet cipher instance.
    """
    # Convert any key string into a valid Fernet key
    key = hashlib.sha256(settings.ENCRYPTION_KEY.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))


class EmailSummary(models.Model):
    """
    Stores the encrypted AI-generated summary for a client.

    Each client has a single summary record containing:
    - The encrypted summary text
    - The number of emails processed
    - Timestamps for creation and updates

    The summary is encrypted before being stored in the database
    to protect sensitive client information.
    """
    client = models.OneToOneField("clients.Client", on_delete=models.CASCADE, related_name="summary",)
    encrypted_summary = models.TextField()
    emails_processed = models.PositiveIntegerField(default=0)
    last_refreshed = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Metadata for the EmailSummary model.
        """
        db_table = "email_summaries"

    def __str__(self):
        """
        Return a readable representation of the summary record.
        """
        return f"Summary - {self.client.name}"

    @property
    def decrypted_summary(self):
        """
        Decrypt and return the stored email summary.

        Returns:
            str: Decrypted summary text.
        """
        cipher = get_cipher()
        return cipher.decrypt(self.encrypted_summary.encode()).decode()

    def set_summary(self, text):
        """
        Encrypt the provided summary text and store it in the model.

        Args:
            text (str): Plain text summary to be encrypted.
        """
        cipher = get_cipher()
        self.encrypted_summary = cipher.encrypt(text.encode()).decode()