from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Client

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import ClientSerializer

from .models import Client
from apps.emails.models import Email
from apps.summaries.models import EmailSummary
from apps.summaries.utils.encryption import decrypt
import json


class ClientListAPIView(generics.ListAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Client.objects.all()
        return Client.objects.filter(firm=user.firm)


class ClientDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Client.objects.all()
        return Client.objects.filter(firm=user.firm)

@login_required
def client_list(request):
    clients = Client.objects.select_related("firm").all()

    context = { "clients": clients }

    return render(request, "clients/list.html", context)


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client.objects.select_related("firm"), pk=pk)

    emails = Email.objects.filter(client=client).order_by("sent_at")
    summary = EmailSummary.objects.filter(client=client).first()
    summary_data = None

    if summary:
        summary_data = json.loads(decrypt(summary.encrypted_summary))
    context = {
        "client": client,
        "emails": emails,
        "summary": summary_data,
    }

    return render(request, "clients/detail.html", context)