from django.shortcuts import render

import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.clients.models import Client
from apps.emails.models import Email
from .models import EmailSummary

from .services.summarizer import generate_summary
from .utils.encryption import encrypt
from django.core.cache import cache
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


class GenerateSummaryAPIView(APIView):
    """
    API view to generate email summary for a specific client.

    Workflow:
    - Checks Redis cache first
    - If not found, generates summary from emails
    - Stores summary in Redis (cache)
    - Encrypts summary and stores in database

    Returns:
    - cached summary if available
    - otherwise newly generated summary
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        Handle POST request to generate or fetch email summary.
        """
        cache_key = f"summary_{pk}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response({
                "source": "cache",
                "data": cached_data
            })

        client = Client.objects.get(id=pk)
        emails = Email.objects.filter(client=client)

        if not emails.exists():
            return Response({"error": "No emails found"})

        summary_data = generate_summary(emails)

        cache.set(cache_key, summary_data, timeout=3600)

        encrypted = encrypt(json.dumps(summary_data))

        summary_obj, created = EmailSummary.objects.get_or_create(
            client=client,
            defaults={
                "encrypted_summary": encrypted,
                "emails_processed": emails.count(),
            }
        )

        if not created:
            summary_obj.encrypted_summary = encrypted
            summary_obj.emails_processed = emails.count()
            summary_obj.save()

        return Response({
            "source": "generated",
            "data": summary_data
        })


class RefreshSummaryAPIView(APIView):
    """
    API view to refresh email summary for a client.

    Clears cached summary and regenerates it.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        Handle POST request to refresh summary.
        """
        cache.delete(f"summary_{pk}")

        generator = GenerateSummaryAPIView()
        return generator.post(request, pk)


@login_required
def generate_summary_page(request, pk):
    """
    Generate email summary for a client via web page.

    Steps:
    - Fetch client emails
    - Generate summary
    - Store in Redis cache
    - Encrypt and save in database
    - Redirect to client detail page
    """
    client = get_object_or_404(Client, pk=pk)

    emails = Email.objects.filter(client=client)

    if not emails.exists():
        return redirect("client-detail", pk=pk)

    summary_data = generate_summary(emails)

    cache.set(f"summary_{pk}", summary_data, timeout=3600)

    encrypted = encrypt(json.dumps(summary_data))

    summary, created = EmailSummary.objects.get_or_create(client=client)

    summary.encrypted_summary = encrypted
    summary.emails_processed = emails.count()
    summary.save()

    return redirect("client-detail", pk=pk)


@login_required
def refresh_summary_page(request, pk):
    """
    Refresh email summary from web interface.

    Actions:
    - Delete cached summary
    - Delete existing DB summary
    - Regenerate fresh summary
    """
    cache.delete(f"summary_{pk}")
    EmailSummary.objects.filter(client_id=pk).delete()

    return generate_summary_page(request, pk)