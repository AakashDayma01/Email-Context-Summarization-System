from django.urls import path

from .views import firm_report, global_report, firm_report, FirmReportAPIView, GlobalReportAPIView

urlpatterns = [
    path("", firm_report, name="report-dashboard",),
    path("firm/", firm_report, name="firm-report"),
    path("global/", global_report, name="global-report-page",),
    path("api/", FirmReportAPIView.as_view(), name="firm-report-api",),
    path("api/global/", GlobalReportAPIView.as_view(), name="global-report-api",),
]