"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.reports.views import (
    dashboard,
    FirmReportAPIView,
    GlobalReportAPIView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from apps.accounts.views import login_view, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", dashboard, name="dashboard"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("clients/", include("apps.clients.urls")),
    path("summary/", include("apps.summaries.urls")),
    path("reports/", include("apps.reports.urls")),    

    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),

    path("api/clients/", include("apps.clients.api_urls")),
    path("api/", include("apps.emails.urls")),

    path("api/", include("apps.emails.urls")),
    path("api/", include("apps.summaries.urls")),

    path("api/reports/", include("apps.reports.urls")),


    path("api/schema/", SpectacularAPIView.as_view(), name="schema",),

    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui",),
]