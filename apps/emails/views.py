from django.shortcuts import render,get_object_or_404, redirect

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Email
from .serializers import EmailSerializer
from apps.clients.models import Client
from django.contrib.auth.decorators import login_required

from .models import Email
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

        return Email.objects.filter(client=client, client__firm=user.firm)
    
@login_required
def add_mock_email(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        Email.objects.create(client=client, accountant=request.user, subject=request.POST["subject"], body=request.POST["body"])
    return redirect("client-detail", pk=pk)