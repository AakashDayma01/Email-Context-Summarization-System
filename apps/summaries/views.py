import json

from django.core.cache import cache
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clients.services.permissions import get_clients_for_user
from apps.emails.services.permissions import get_emails_for_user

from .models import EmailSummary
from .services.summarizer import generate_summary
from .utils.encryption import encrypt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class GenerateSummaryAPIView(APIView):                      
    """
    Generate an AI-powered summary for a client's email history.

    Workflow:
    ----------
    1. Validate the authenticated user's access to the client.
    2. Retrieve emails visible to the user.
    3. Check Redis cache for an existing summary.
    4. If cache exists, return the cached summary.
    5. Otherwise, generate a new summary using the AI service.
    6. Cache the generated summary in Redis.
    7. Encrypt and store the summary in PostgreSQL.
    8. Return the generated summary.

    Access Rules:
    -------------
    - Super Admin -> Any client
    - Accountant -> Assigned clients only
    - Client -> Own client only
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Generate Email Summary",
        operation_description="""
        This API generates an AI-powered summary for a client.

        Flow:
        - Fetch emails for the client
        - Check Redis cache
        - If not found → fetch DB
        - If outdated → regenerate using Gemini AI
        - Store result in Redis + PostgreSQL
        """,
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="Client ID",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response(description="Summary generated successfully"),
            404: "Client or emails not found"
        }
    )
    def post(self, request, pk):
        """
        Generate or retrieve a cached summary for a client.

        Args:
            request: Authenticated HTTP request.
            pk (int): Client primary key.

        Returns:
            Response:
                - Cached summary if available.
                - Newly generated summary otherwise.
        """
        client = get_object_or_404(
            get_clients_for_user(request.user),
            pk=pk
        )

        emails = get_emails_for_user(request.user, client)

        if not emails.exists():
            return Response({"error": "No emails found."}, status=404)

        cache_key = f"summary_{client.id}"
        cached_summary = cache.get(cache_key)

        if cached_summary:
            print("DATA FROM REDIS")
            return Response({
                "source": "cache",
                "summary": cached_summary
            })

        print("DATA FROM GENERATION")

        summary_data = generate_summary(emails)

        cache.set(cache_key, summary_data, timeout=3600)

        encrypted_summary = encrypt(json.dumps(summary_data))

        summary, created = EmailSummary.objects.get_or_create(
            client=client,
            defaults={
                "encrypted_summary": encrypted_summary,
                "emails_processed": emails.count(),
            },
        )

        if not created:
            summary.encrypted_summary = encrypted_summary
            summary.emails_processed = emails.count()
            summary.save()

        return Response({
            "source": "generated",
            "summary": summary_data
        })


class RefreshSummaryAPIView(APIView):
    """
    Regenerate a client's email summary.

    Workflow:
    ----------
    1. Validate user permissions.
    2. Remove the existing Redis cache.
    3. Delete the existing database summary.
    4. Generate a completely new summary.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        client = get_object_or_404(
            get_clients_for_user(request.user),
            pk=pk
        )

        cache.delete(f"summary_{client.id}")

        summary = EmailSummary.objects.filter(
            client=client
        ).first()

        if summary:
            summary.delete()

        return GenerateSummaryAPIView().post(request, pk)

