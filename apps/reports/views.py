from django.shortcuts import render
from apps.emails.models import Email

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.clients.models import Client
from apps.summaries.models import EmailSummary

from django.contrib.auth.decorators import login_required
from collections import defaultdict


class FirmReportAPIView(APIView):
    """
    API view to generate summary report for a specific firm.

    Returns:
    - total number of clients in the user's firm
    - number of clients that have generated email summaries

    Only authenticated users can access this endpoint.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handle GET request and return firm-level analytics.
        """
        user = request.user

        clients = Client.objects.filter(firm=user.firm)
        total_clients = clients.count()

        clients_with_summary = EmailSummary.objects.filter(
            client__in=clients
        ).count()

        return Response({
            "firm": user.firm.name,
            "total_clients": total_clients,
            "clients_with_summary": clients_with_summary
        })


class GlobalReportAPIView(APIView):
    """
    API view to generate system-wide summary report.

    Only superusers can access this endpoint.

    Returns number of email summaries grouped by firm.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handle GET request and return summary count per firm.
        """
        if not request.user.is_superuser:
            return Response({"error": "Not allowed"}, status=403)

        data = defaultdict(int)

        summaries = EmailSummary.objects.all().select_related("client__firm")

        for summary in summaries:
            firm_name = summary.client.firm.name
            data[firm_name] += 1

        return Response([
            {"firm": k, "summaries": v}
            for k, v in data.items()
        ])


@login_required
def dashboard(request):
    """
    Render system dashboard with overall statistics.

    Displays:
    - total clients
    - total emails
    - total email summaries
    """
    context = {
        "total_clients": Client.objects.count(),
        "total_emails": Email.objects.count(),
        "total_summaries": EmailSummary.objects.count(),
    }

    return render(request, "dashboard.html", context)


@login_required
def firm_report(request):
    """
    Render firm-level report for logged-in user.

    Shows:
    - total clients in firm
    - number of clients with email summaries
    """
    clients = Client.objects.filter(firm=request.user.firm)

    total_clients = clients.count()

    clients_with_summary = EmailSummary.objects.filter(
        client__in=clients
    ).count()

    return render(
        request,
        "reports/firm_report.html",
        {
            "firm": request.user.firm,
            "total_clients": total_clients,
            "clients_with_summary": clients_with_summary,
        },
    )


@login_required
def global_report(request):
    """
    Render global report page (superuser only).

    Displays number of email summaries grouped by firm.
    """
    if not request.user.is_superuser:
        return render(request, "reports/not_allowed.html")

    data = defaultdict(int)

    summaries = EmailSummary.objects.select_related("client__firm")

    for summary in summaries:
        data[summary.client.firm.name] += 1

    reports = [
        {"firm": firm, "count": count}
        for firm, count in data.items()
    ]

    return render(
        request,
        "reports/global_report.html",
        {
            "reports": reports
        },
    )