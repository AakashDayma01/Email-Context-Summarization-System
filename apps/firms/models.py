from django.db import models

# Create your models here.
from django.db import models


class Firm(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "firms"

    def __str__(self):
        return self.name