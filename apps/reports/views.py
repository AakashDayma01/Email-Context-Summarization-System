from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clients.models import Client
from apps.emails.models import Email
from apps.summaries.models import EmailSummary


# =========================================================
# API : FIRM REPORT
# =========================================================
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


# =========================================================
# API : GLOBAL REPORT
# =========================================================
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


# =========================================================
# TEMPLATE : DASHBOARD
# =========================================================
@login_required
def dashboard(request):
    """
    Render dashboard based on user role.

    Access Rules:
    - Super Admin -> Entire system
    - Accountant -> Assigned clients
    - Client -> Not allowed
    """

    user = request.user

    if (
        not user.is_superuser
        and user.role == user.Role.CLIENT
    ):
        return render(
            request,
            "reports/not_allowed.html",
        )

    if user.is_superuser:

        context = {
            "total_clients": Client.objects.count(),
            "total_emails": Email.objects.count(),
            "total_summaries": EmailSummary.objects.count(),
        }

    else:

        clients = Client.objects.filter(
            accountants=user
        ).distinct()

        context = {
            "total_clients": clients.count(),
            "total_emails": Email.objects.filter(
                client__in=clients
            ).count(),
            "total_summaries": EmailSummary.objects.filter(
                client__in=clients
            ).count(),
        }

    return render(
        request,
        "dashboard.html",
        context,
    )


# =========================================================
# TEMPLATE : FIRM REPORT
# =========================================================
@login_required
def firm_report(request):
    """
    Display report for accessible clients.

    Access Rules:
    - Super Admin -> All clients
    - Accountant -> Assigned clients
    - Client -> Not allowed
    """

    user = request.user

    if (
        not user.is_superuser
        and user.role == user.Role.CLIENT
    ):
        return render(
            request,
            "reports/not_allowed.html",
        )

    if user.is_superuser:

        clients = Client.objects.all()
        firm = "All Firms"

    else:

        clients = Client.objects.filter(
            accountants=user
        ).distinct()

        firm = user.firm

    total_clients = clients.count()

    clients_with_summary = EmailSummary.objects.filter(
        client__in=clients
    ).count()

    return render(
        request,
        "reports/firm_report.html",
        {
            "firm": firm,
            "total_clients": total_clients,
            "clients_with_summary": clients_with_summary,
        },
    )


# =========================================================
# TEMPLATE : GLOBAL REPORT
# =========================================================
@login_required
def global_report(request):
    """
    Display system-wide report.

    Access Rules:
    - Super Admin -> Allowed
    - Accountant -> Not allowed
    - Client -> Not allowed
    """

    if not request.user.is_superuser:
        return render(
            request,
            "reports/not_allowed.html",
        )

    data = defaultdict(int)

    summaries = (
        EmailSummary.objects
        .select_related("client__firm")
    )

    for summary in summaries:
        data[summary.client.firm.name] += 1

    reports = [
        {
            "firm": firm,
            "count": count,
        }
        for firm, count in data.items()
    ]

    return render(
        request,
        "reports/global_report.html",
        {
            "reports": reports,
        },
    )