from django.shortcuts import render

# Create your views here.
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



import json

class GenerateSummaryAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        cache_key = f"summary_{pk}"

        # 1. Check cache first
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

        # 2. Generate summary
        summary_data = generate_summary(emails)

        # 3. Encrypt
        encrypted = encrypt(json.dumps(summary_data))

        # 4. Save DB
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

        # 5. Store cache (IMPORTANT)
        cache.set(cache_key, summary_data, timeout=3600)

        return Response({
            "source": "db",
            "data": summary_data
        })
    
    
class RefreshSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        cache.delete(f"summary_{pk}")

        generator = GenerateSummaryAPIView()
        return generator.post(request, pk)
    


@login_required
def generate_summary_page(request, pk):

    client = get_object_or_404(Client, pk=pk)

    emails = Email.objects.filter(client=client)

    if not emails.exists():
        return redirect("client-detail-page", pk=pk)

    summary_data = generate_summary(emails)

    encrypted = encrypt(json.dumps(summary_data))

    summary, created = EmailSummary.objects.get_or_create(
        client=client
    )

    summary.encrypted_summary = encrypted
    summary.emails_processed = emails.count()
    summary.save()

    cache.set(
        f"summary_{pk}",
        summary_data,
        timeout=3600
    )
    return redirect("client-detail", pk=pk)




@login_required
def refresh_summary_page(request, pk):

    # Remove cached summary
    cache.delete(f"summary_{pk}")

    # Remove existing summary from database
    EmailSummary.objects.filter(client_id=pk).delete()

    # Generate a new summary
    return generate_summary_page(request, pk)