from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
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


# =========================================================
# API : CLIENT LIST
# =========================================================
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


# =============================c============================
# API : CLIENT DETAIL
# =========================================================
from rest_framework.response import Response
from django.core.cache import cache
import json

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

        # -------------------------
        # STEP 1: REDIS CHECK
        # -------------------------
        summary_data = cache.get(cache_key)

        if summary_data:
            print("🚀 API SUMMARY SOURCE: REDIS")
            return Response({
                "source": "redis",
                "client": ClientSerializer(client).data,
                "summary": summary_data,
            })

        print("⚠️ API REDIS MISS - checking DB")

        # -------------------------
        # STEP 2: DB CHECK
        # -------------------------
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

        # -------------------------
        # STEP 3: GENERATE NEW
        # -------------------------
        print("⚠️ NO CACHE / DB → generating summary")

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

# =========================================================
# TEMPLATE : CLIENT LIST
# =========================================================
@login_required
def client_list(request):
    """
    Display clients visible to the logged-in user.
    """

    clients = get_clients_for_user(request.user)

    return render(
        request,
        "clients/list.html",
        {
            "clients": clients
        },
    )


# =========================================================
# TEMPLATE : CLIENT DETAIL
# =========================================================
@login_required
def client_detail(request, pk):
    """
    Display client details and email summary.

    Workflow:
    1. Verify user permission.
    2. Retrieve emails visible to the user.
    3. Check Redis cache.
    4. Check PostgreSQL summary.
    5. Regenerate summary if emails changed.
    6. Cache regenerated summary.
    7. Render client page.
    """

    # ----------------------------------------
    # Permission check
    # ----------------------------------------
    client = get_object_or_404(
        get_clients_for_user(request.user),
        pk=pk,
    )

    # ----------------------------------------
    # Retrieve permitted emails
    # ----------------------------------------
    emails = get_emails_for_user(
        request.user,
        client,
    )

    email_count = emails.count()

    cache_key = f"summary_{client.id}"

    # ----------------------------------------
    # Step 1 : Check Redis
    # ----------------------------------------
    summary_data = cache.get(cache_key)

    if summary_data:
        print("🚀 SUMMARY SOURCE: REDIS CACHE")
    else:
        print("⚠️ REDIS MISS - checking database")
    # ----------------------------------------
    # Step 2 : Fetch PostgreSQL summary
    # ----------------------------------------
    summary = (
        EmailSummary.objects
        .filter(client=client)
        .first()
    )

    # ----------------------------------------
    # Step 3 : Determine regeneration
    # ----------------------------------------
    regenerate = (
        summary is None or
        summary.emails_processed != email_count
    )

    # ----------------------------------------
    # Step 4 : Generate summary
    # ----------------------------------------
    if regenerate:

        summary_data = generate_summary(emails)

        cache.set(
            cache_key,
            summary_data,
            timeout=3600,
        )

        encrypted_summary = encrypt(
            json.dumps(summary_data)
        )

        if summary is None:

            EmailSummary.objects.create(
                client=client,
                encrypted_summary=encrypted_summary,
                emails_processed=email_count,
            )

        else:

            summary.encrypted_summary = encrypted_summary
            summary.emails_processed = email_count
            summary.save()

    # ----------------------------------------
    # Step 5 : Redis Miss
    # ----------------------------------------
    elif summary_data is None:

        summary_data = json.loads(
            decrypt(summary.encrypted_summary)
        )

        cache.set(
            cache_key,
            summary_data,
            timeout=3600,
        )

    # ----------------------------------------
    # Step 6 : Render page
    # ----------------------------------------
    return render(
        request,
        "clients/detail.html",
        {
            "client": client,
            "emails": emails,
            "summary": summary_data,
        },
    )