from django.urls import path

from .views import GenerateSummaryAPIView, generate_summary_page,refresh_summary_page, RefreshSummaryAPIView

urlpatterns = [
    path("<int:pk>/summary/", GenerateSummaryAPIView.as_view(),  name="generate-summary-api",),
    path("<int:pk>/summary/refresh/", RefreshSummaryAPIView.as_view(), name="refresh-summary"),
    #path("generate/<int:pk>/", generate_summary_page, name="generate-summary-page",),
    #path("refresh/<int:pk>/", refresh_summary_page, name="refresh-summary-page",),
]