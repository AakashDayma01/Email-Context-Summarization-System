from django.urls import path
from .views import ClientEmailListAPIView 

urlpatterns = [
    path("<int:pk>/emails/", ClientEmailListAPIView.as_view()),
]