from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import EmailSerializer

from apps.clients.services.permissions import get_clients_for_user
from apps.emails.services.permissions import get_emails_for_user


# API : CLIENT EMAIL LIST
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

