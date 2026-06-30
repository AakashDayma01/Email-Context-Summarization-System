from django.conf import settings
from django.db import models


class Client(models.Model):
    """
    Represents a client belonging to a firm.

    Every client belongs to one firm and has one login account.

    A client may be assigned to one or more accountants who can
    manage emails, summaries, and communication for that client.
    """

    # Firm that owns the client
    firm = models.ForeignKey(
        "firms.Firm",
        on_delete=models.CASCADE,
        related_name="clients",
    )

    # Login account for the client
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="client_profile",
        limit_choices_to={"role": "CLIENT"},
        null=True,
        blank=True,
    )

    # Accountants assigned to this client
    accountants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="assigned_clients",
        limit_choices_to={"role": "ACCOUNTANT"},
        blank=True,
    )

    name = models.CharField(max_length=255)

    email = models.EmailField(unique=True)

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "clients"
        ordering = ["name"]

    def __str__(self):
        return self.name