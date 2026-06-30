from django.core.cache import cache
import json

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Client
from .serializers import ClientSerializer

from apps.emails.services.permissions import get_emails_for_user
from apps.clients.services.permissions import get_clients_for_user

from apps.summaries.models import EmailSummary
from apps.summaries.services.summarizer import generate_summary
from apps.summaries.utils.encryption import encrypt, decrypt

from rest_framework.response import Response

# API : CLIENT LIST
class ClientListAPIView(generics.ListAPIView):
    """
    Retrieve clients based on the authenticated user's permissions.

    Access Rules:
    - Super Admin -> All clients
    - Accountant -> Assigned clients only
    - Client -> Own client profile only
    """

    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_clients_for_user(self.request.user)


# API : CLIENT DETAIL
class ClientDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieve a single client with cached email summary.

    Flow:
    1. Check Redis cache
    2. If miss → check DB encrypted summary
    3. If still missing/outdated → regenerate
    """

    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_clients_for_user(self.request.user)

    def retrieve(self, request, *args, **kwargs):
        client = self.get_object()

        emails = get_emails_for_user(request.user, client)
        email_count = emails.count()

        cache_key = f"summary_{client.id}"

        # STEP 1: REDIS CHECK
        summary_data = cache.get(cache_key)

        if summary_data:
            print("🚀 API SUMMARY SOURCE: REDIS")
            return Response({
                "source": "redis",
                "client": ClientSerializer(client).data,
                "summary": summary_data,
            })

        # STEP 2: DB CHECK
        summary = EmailSummary.objects.filter(client=client).first()

        if summary:
            print("🗄️ API SUMMARY SOURCE: DATABASE")

            summary_data = json.loads(
                decrypt(summary.encrypted_summary)
            )

            # store back into redis
            cache.set(cache_key, summary_data, timeout=3600)

            return Response({
                "source": "database",
                "client": ClientSerializer(client).data,
                "summary": summary_data,
            })

        summary_data = generate_summary(emails)

        cache.set(cache_key, summary_data, timeout=3600)

        encrypted_summary = encrypt(json.dumps(summary_data))

        EmailSummary.objects.create(
            client=client,
            encrypted_summary=encrypted_summary,
            emails_processed=email_count,
        )

        return Response({
            "source": "generated",
            "client": ClientSerializer(client).data,
            "summary": summary_data,
        })
