from django.urls import path
from .views import ClientEmailListAPIView, add_mock_email
urlpatterns = [
    path("<int:pk>/emails/", ClientEmailListAPIView.as_view()),
    path("add/<int:pk>/",  add_mock_email, name="add-email", ),
]