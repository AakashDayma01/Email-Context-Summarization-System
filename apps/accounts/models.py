# from django.contrib.auth.models import AbstractUser
# from django.db import models


# class Account(AbstractUser):
#     """
#     Custom user model for the Email Context & Summarization System.

#     This model extends Django's AbstractUser to support:
#     - Email-based authentication
#     - Firm association for multi-tenant data isolation
#     - Role-based user management

#     Each account belongs to a firm (optional for superusers) and
#     is assigned a role that determines its level of access.
#     """

#     class Role(models.TextChoices):
#         """
#         Available roles for system users.
#         """
#         ACCOUNTANT = "ACCOUNTANT", "Accountant"
#         ADMIN = "ADMIN", "Admin"
#         SUPERUSER = "SUPERUSER", "Superuser"

#     email = models.EmailField(unique=True)

#     firm = models.ForeignKey(
#         "firms.Firm",
#         on_delete=models.CASCADE,
#         related_name="accountants",
#         null=True,
#         blank=True,
#     )

#     role = models.CharField(
#         max_length=20,
#         choices=Role.choices,
#         default=Role.ACCOUNTANT,
#     )

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username"]

#     class Meta:
#         """
#         Metadata for the Account model.
#         """
#         db_table = "accounts"

#     def __str__(self):
#         """
#         Return the email address as the string representation
#         of the account.
#         """
#         return self.email


from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    """
    Custom user model for Email Context & Summarization System.

    Supports:
    - Email authentication
    - Multi-tenant firm association
    - Role-based access control
    """

    class Role(models.TextChoices):
        """
        System roles inside a firm.
        """
        FIRM_ADMIN = "FIRM_ADMIN", "Firm Admin"
        ACCOUNTANT = "ACCOUNTANT", "Accountant"

    # 🔹 Login using email
    email = models.EmailField(unique=True)

    # 🔹 Multi-tenant: user belongs to a firm (client)
    firm = models.ForeignKey(
        "firms.Firm",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )

    # 🔹 Role inside firm
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ACCOUNTANT,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "accounts"

    def __str__(self):
        return self.email