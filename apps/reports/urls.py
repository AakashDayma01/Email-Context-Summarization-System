from django.urls import path
from .views import FirmReportAPIView, GlobalReportAPIView

urlpatterns = [
    path("api/", FirmReportAPIView.as_view(), name="firm-report-api",),
    path("api/global/", GlobalReportAPIView.as_view(), name="global-report-api",),
]