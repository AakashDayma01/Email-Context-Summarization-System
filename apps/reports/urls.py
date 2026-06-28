from django.urls import path
from .views import dashboard, reports_page, FirmReportAPIView, GlobalReportAPIView

urlpatterns = [
    path("", reports_page, name="report-dashboard"),
    path("firm/", FirmReportAPIView.as_view()),
    path("global/", GlobalReportAPIView.as_view()),
]