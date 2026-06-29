from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Client

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import ClientSerializer

from apps.emails.models import Email
from apps.summaries.models import EmailSummary
from apps.summaries.utils.encryption import decrypt
from django.core.cache import cache
import json
from apps.summaries.services.summarizer import generate_summary
from apps.summaries.utils.encryption import encrypt


class ClientListAPIView(generics.ListAPIView):
    """
    API view to retrieve a list of clients.

    Superusers can access all clients, while regular users
    can only access clients belonging to their firm.
    """
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return queryset of clients based on user permissions.
        """
        user = self.request.user

        if user.is_superuser:
            return Client.objects.all()
        return Client.objects.filter(firm=user.firm)


class ClientDetailAPIView(generics.RetrieveAPIView):
    """
    API view to retrieve a single client detail.

    Access is restricted based on user permissions:
    superusers can access all clients, others only their firm clients.
    """
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return queryset of clients based on user permissions.
        """
        user = self.request.user

        if user.is_superuser:
            return Client.objects.all()
        return Client.objects.filter(firm=user.firm)


@login_required
def client_list(request):
    """
    Render a list of clients for authenticated users.

    Superusers can see all clients, while normal users
    can only see clients associated with their firm.
    """
    if request.user.is_superuser:
        clients = Client.objects.select_related("firm").all()
    else:
        clients = Client.objects.select_related("firm").filter(firm=request.user.firm)

    return render(request, "clients/list.html", {"clients": clients})

@login_required
def client_detail(request, pk):
    """
    Display client details along with the latest email summary.

    Workflow:
    1. Fetch the client and all associated emails.
    2. Check Redis for a cached summary.
    3. Read summary metadata from PostgreSQL.
    4. Compare current email count with emails_processed.
    5. If outdated, regenerate the summary.
    6. Otherwise use Redis if available.
    7. If Redis is empty, decrypt PostgreSQL summary and cache it.
    """
    client = get_object_or_404(
        Client.objects.select_related("firm"),
        pk=pk
    )

    emails = (
        Email.objects
        .filter(client=client)
        .order_by("sent_at")
    )

    email_count = emails.count()

    cache_key = f"summary_{client.id}"

    # ----------------------------
    # STEP 1 : Check Redis
    # ----------------------------
    summary_data = cache.get(cache_key)
    
    # ----------------------------
    # STEP 2 : Get summary metadata
    # ----------------------------
    summary = (
        EmailSummary.objects
        .only("encrypted_summary", "emails_processed")
        .filter(client=client)
        .first()
    )

    # ----------------------------
    # STEP 3 : Determine whether
    # summary needs regeneration
    # ----------------------------
    regenerate = False

    if summary is None:
        regenerate = True

    elif summary.emails_processed != email_count:
        regenerate = True

    # ----------------------------
    # STEP 4 : Regenerate summary
    # ----------------------------
    if regenerate:

        summary_data = generate_summary(emails)

        # Update Redis
        cache.set(
            cache_key,
            summary_data,
            timeout=3600
        )

        encrypted_summary = encrypt(
            json.dumps(summary_data)
        )

        if summary is None:

            EmailSummary.objects.create(
                client=client,
                encrypted_summary=encrypted_summary,
                emails_processed=email_count
            )

        else:

            summary.encrypted_summary = encrypted_summary
            summary.emails_processed = email_count
            summary.save()

    # ----------------------------
    # STEP 5 : Redis miss
    # ----------------------------
    elif summary_data is None:
        summary_data = json.loads(
            decrypt(summary.encrypted_summary)
        )

        cache.set(
            cache_key,
            summary_data,
            timeout=3600
        )
    # ----------------------------
    # STEP 6 : Render page
    # ----------------------------
    context = {
        "client": client,
        "emails": emails,
        "summary": summary_data,
    }

    return render(
        request,
        "clients/detail.html",
        context
    )