"""
URL configuration for testapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from api.views import user_login, user_logout

# Redirect '/' to login page
def redirect_to_login(request):
    return redirect("login")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),  # Include API URLs
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("dashboard/", login_required(TemplateView.as_view(template_name="dashboard.html")), name="dashboard"),
    path("", redirect_to_login, name="home"),  # ✅ Redirect empty path `/` to login page
]
