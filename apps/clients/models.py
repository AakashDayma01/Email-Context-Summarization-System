from django.db import models

# Create your models here.
from django.db import models


class Client(models.Model):

    firm = models.ForeignKey(
        "firms.Firm",
        on_delete=models.CASCADE,
        related_name="clients",
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

    def __str__(self):
        return self.name