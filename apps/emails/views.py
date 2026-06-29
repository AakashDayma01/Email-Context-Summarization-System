from django.shortcuts import render,get_object_or_404, redirect

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render, get_object_or_404, redirect

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Email
from .serializers import EmailSerializer
from apps.clients.models import Client
from django.contrib.auth.decorators import login_required


class ClientEmailListAPIView(generics.ListAPIView):
    """
    API view to list all emails related to a specific client.

    Superusers can access all emails for the client,
    while normal users can only access emails belonging to clients
    within their firm.
    """
    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return emails for a specific client based on user permissions.
        """
        user = self.request.user
        client_id = self.kwargs["pk"]

        client = Client.objects.get(id=client_id)

        if user.is_superuser:
            return Email.objects.filter(client=client)

        return Email.objects.filter(client=client, client__firm=user.firm)


@login_required
def add_mock_email(request, pk):
    """
    Create a mock email entry for a specific client.

    This view allows authenticated users to add an email
    (subject and body) for a given client. After creation,
    the user is redirected to the client detail page.
    """
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        Email.objects.create(
            client=client,
            accountant=request.user,
            subject=request.POST["subject"],
            body=request.POST["body"]
        )

    return redirect("client-detail", pk=pk)