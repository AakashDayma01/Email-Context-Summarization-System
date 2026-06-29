from django.db import models

# Create your models here.
from django.db import models


class Firm(models.Model):
    """
    Represents an accounting firm within the system.

    A firm serves as a tenant in the multi-tenant architecture.
    Each firm can have multiple accountants and clients, ensuring
    that data is isolated between different organizations.
    """
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "firms"

    def __str__(self):
        return self.name