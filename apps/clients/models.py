from django.db import models


class Client(models.Model):
    """
    Represents a client belonging to a firm.

    Each client stores basic contact information and is associated
    with a single firm. Client records are used to organize emails
    and generate contextual summaries within the system.
    """

    firm = models.ForeignKey(
        "firms.Firm",
        on_delete=models.CASCADE,
        related_name="clients"
    )

    name = models.CharField(max_length=255)

    email = models.EmailField(unique=True)

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Metadata for the Client model.
        """
        db_table = "clients"

    def __str__(self):
        """
        Return the client's name as its string representation.
        """
        return self.name