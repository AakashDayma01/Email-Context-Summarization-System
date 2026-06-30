from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    """
    Custom user model for the Email Context & Summarization System.

    Features:
    - Email-based authentication
    - Multi-tenant firm association
    - Role-based access (Accountant / Client)
    - Django's built-in is_superuser is used for the System Administrator
    """

    class Role(models.TextChoices):
        """
        Application roles.
        Super Admin is handled using Django's built-in is_superuser field.
        """
        ACCOUNTANT = "ACCOUNTANT", "Accountant"
        CLIENT = "CLIENT", "Client"

    # Login using email
    email = models.EmailField(unique=True)

    # Firm to which the user belongs
    # Super Admin can have firm=None
    firm = models.ForeignKey(
        "firms.Firm",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )

    # Application role
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "accounts"
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.email

    @property
    def is_accountant(self):
        """
        Returns True if the user is an accountant.
        """
        return self.role == self.Role.ACCOUNTANT

    @property
    def is_client(self):
        """
        Returns True if the user is a client.
        """
        return self.role == self.Role.CLIENT

    @property
    def is_system_admin(self):
        """
        Returns True if the user is Django Super Admin.
        """
        return self.is_superuser