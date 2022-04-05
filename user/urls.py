"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from user.views import MyTokenObtainPairView, SiteUserView, UpdateProfile, AdminUserView, ListAllFields

urlpatterns = [
    path("api/user/", SiteUserView.as_view(), name="createaccount"),
    path("api/token/", MyTokenObtainPairView.as_view(), name="ObtainedToken"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="RefreshToken"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="RefreshToken"),
    path("api/user/upload_profile_image/", UpdateProfile.as_view(), name="createaccount"),
    # Admin User
    path("api/admin/user/", AdminUserView.as_view({"get":"list","post":"create"}), name="adminUser"),
    path("api/admin/user/<int:pk>", AdminUserView.as_view({"delete":"destroy","patch":"update"}), name="adminUsesr"),

    path("api/list/keys/",ListAllFields.as_view())
]
