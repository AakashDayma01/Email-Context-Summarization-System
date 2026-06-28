from django.urls import path
from .views import client_list, client_detail

urlpatterns = [
    path("", client_list, name="client-list"),
    path("<int:pk>/", client_detail, name="client-detail"),
]

