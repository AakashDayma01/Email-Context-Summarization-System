from django.urls import path

from .views import GenerateSummaryAPIView, RefreshSummaryAPIView

urlpatterns = [
    path("<int:pk>/summary/", GenerateSummaryAPIView.as_view(),  name="generate-summary-api",),
    path("<int:pk>/summary/refresh/", RefreshSummaryAPIView.as_view(), name="refresh-summary"),
]