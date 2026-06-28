from django.shortcuts import render
from apps.emails.models import Email
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.clients.models import Client
from apps.summaries.models import EmailSummary

from django.contrib.auth import get_user_model
from collections import defaultdict
from django.contrib.auth.decorators import login_required


class FirmReportAPIView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        # only firm admins
        clients = Client.objects.filter(firm=user.firm)
        total_clients = clients.count()
        clients_with_summary = EmailSummary.objects.filter(client__in=clients).count()
        return Response({"firm": user.firm.name,"total_clients": total_clients, "clients_with_summary": clients_with_summary})




class GlobalReportAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if not request.user.is_superuser:
            return Response({"error": "Not allowed"}, status=403)
        data = defaultdict(int)
        summaries = EmailSummary.objects.all().select_related("client__firm")
        for summary in summaries:
            firm_name = summary.client.firm.name
            data[firm_name] += 1

        return Response([{"firm": k, "summaries": v} for k, v in data.items()])
    


@login_required
def dashboard(request):
    context = {
        "total_clients": Client.objects.count(),
        "total_emails": Email.objects.count(),
        "total_summaries": EmailSummary.objects.count(),
    }

    return render(request, "dashboard.html", context)



# @login_required
# def reports_page(request):

#     user = request.user

#     if user.is_superuser:
#         total_clients = Client.objects.count()
#         total_summaries = EmailSummary.objects.count()
#         firm = "All Firms"
#     else:
#         clients = Client.objects.filter(firm=user.firm)
#         total_clients = clients.count()
#         total_summaries = EmailSummary.objects.filter(
#             client__in=clients
#         ).count()
#         firm = user.firm.name

#     context = {
#         "firm": firm,
#         "total_clients": total_clients,
#         "total_summaries": total_summaries,
#     }

#     return render(request, "reports/index.html", context)



@login_required
def firm_report(request):

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

    if not request.user.is_superuser:
        return render(
            request,
            "reports/not_allowed.html",
        )

    data = defaultdict(int)

    summaries = EmailSummary.objects.select_related(
        "client__firm"
    )

    for summary in summaries:
        data[summary.client.firm.name] += 1

    reports = []

    for firm, count in data.items():
        reports.append(
            {
                "firm": firm,
                "count": count,
            }
        )

    return render(
        request,
        "reports/global_report.html",
        {
            "reports": reports
        },
    )