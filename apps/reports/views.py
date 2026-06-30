from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clients.models import Client
from apps.summaries.models import EmailSummary


# API : FIRM REPORT
class FirmReportAPIView(APIView):
    """
    Return report for the authenticated user's accessible clients.

    Access Rules:
    - Super Admin -> All clients
    - Accountant -> Assigned clients only
    - Client -> Not allowed
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        # Clients cannot access reports
        if (
            not user.is_superuser
            and user.role == user.Role.CLIENT
        ):
            return Response(
                {"detail": "Permission denied."},
                status=403,
            )

        if user.is_superuser:
            clients = Client.objects.all()
            firm_name = "All Firms"
        else:
            clients = Client.objects.filter(
                accountants=user
            ).distinct()
            firm_name = user.firm.name

        total_clients = clients.count()

        clients_with_summary = EmailSummary.objects.filter(
            client__in=clients
        ).count()

        return Response({
            "firm": firm_name,
            "total_clients": total_clients,
            "clients_with_summary": clients_with_summary,
        })


# API : GLOBAL REPORT
class GlobalReportAPIView(APIView):
    """
    Return summary count grouped by firm.

    Access Rules:
    - Super Admin -> Allowed
    - Accountant -> Not allowed
    - Client -> Not allowed
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if not request.user.is_superuser:
            return Response(
                {"detail": "Permission denied."},
                status=403,
            )

        data = defaultdict(int)

        summaries = (
            EmailSummary.objects
            .select_related("client__firm")
        )

        for summary in summaries:
            data[summary.client.firm.name] += 1

        return Response([
            {
                "firm": firm,
                "summaries": count,
            }
            for firm, count in data.items()
        ])

