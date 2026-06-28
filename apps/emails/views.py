from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Email
from .serializers import EmailSerializer
from apps.clients.models import Client


class ClientEmailListAPIView(generics.ListAPIView):

    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user
        client_id = self.kwargs["pk"]

        client = Client.objects.get(id=client_id)

        if user.is_superuser:
            return Email.objects.filter(client=client)

        return Email.objects.filter(
            client=client,
            client__firm=user.firm
        )