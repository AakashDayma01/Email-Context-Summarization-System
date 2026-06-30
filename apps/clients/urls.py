from django.urls import path
from .views import client_list, client_detail
from django.urls import path
from .views import  ClientListAPIView, ClientDetailAPIView
urlpatterns = [
   # path("", client_list, name="client-list"),
    #path("<int:pk>/", client_detail, name="client-detail"),
    # API endpoints
    path("", ClientListAPIView.as_view(), name="api-client-list"),
    path("<int:pk>/", ClientDetailAPIView.as_view(), name="api-client-detail"),
]

