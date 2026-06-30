from django.db import models


class Firm(models.Model):
    """
    Represents an accounting firm (tenant) in the system.

    Each firm has:
    - Multiple accountants
    - Multiple clients
    - Independent emails and summaries

    This enables complete data isolation between firms in the
    multi-tenant Email Context & Summarization System.
    """

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "firms"
        ordering = ["name"]
        verbose_name = "Firm"
        verbose_name_plural = "Firms"

    def __str__(self):
        return self.name