from django.urls import path
from .views import (
    ClientListAPIView,
    ClientDetailAPIView,
)

urlpatterns = [
    path("", ClientListAPIView.as_view(), name="api-client-list"),
    path("<int:pk>/", ClientDetailAPIView.as_view(), name="api-client-detail"),
]