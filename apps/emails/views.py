from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Email
from .serializers import EmailSerializer

from apps.clients.services.permissions import get_clients_for_user
from apps.emails.services.permissions import get_emails_for_user


# =========================================================
# API : CLIENT EMAIL LIST
# =========================================================
class ClientEmailListAPIView(generics.ListAPIView):
    """
    Retrieve emails for a specific client.

    Access Rules:
    - Super Admin -> Can view emails of all clients.
    - Accountant -> Can view emails of assigned clients only.
    - Client -> Can view only their own emails.
    """

    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return emails visible to the authenticated user.
        """

        client = get_object_or_404(
            get_clients_for_user(self.request.user),
            pk=self.kwargs["pk"],
        )

        return get_emails_for_user(
            self.request.user,
            client,
        )


# =========================================================
# TEMPLATE : ADD MOCK EMAIL
# =========================================================
@login_required
def add_mock_email(request, pk):
    """
    Create a mock email for a client.

    Access Rules:
    - Super Admin -> Allowed
    - Accountant -> Allowed for assigned clients
    - Client -> Not allowed
    """

    client = get_object_or_404(
        get_clients_for_user(request.user),
        pk=pk,
    )

    # Clients cannot create emails
    if (
        not request.user.is_superuser
        and request.user.role == request.user.Role.CLIENT
    ):
        return HttpResponseForbidden(
            "Clients are not allowed to create emails."
        )

    if request.method == "POST":
        Email.objects.create(
            client=client,
            accountant=request.user,
            subject=request.POST["subject"],
            body=request.POST["body"],
        )

    return redirect(
        "client-detail",
        pk=pk,
    )