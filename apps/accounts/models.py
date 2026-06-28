from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):

    class Role(models.TextChoices):
        ACCOUNTANT = "ACCOUNTANT", "Accountant"
        ADMIN = "ADMIN", "Admin"
        SUPERUSER = "SUPERUSER", "Superuser"

    email = models.EmailField(unique=True)

    firm = models.ForeignKey("firms.Firm", on_delete=models.CASCADE, related_name="accountants", null=True, blank=True,)

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ACCOUNTANT,)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "accounts"

    def __str__(self):
        return self.email