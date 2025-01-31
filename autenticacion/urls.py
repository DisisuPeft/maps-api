from django.contrib import admin
from django.urls import path
from .views import (
    RegisterView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    CheckUser,
    LogoutView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="post"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="post"),
    path("auth/refresh/", CustomTokenRefreshView.as_view(), name="post"),
    path("auth/verify/", CustomTokenVerifyView.as_view(), name="post"),
    path("auth/users/", CheckUser.as_view(), name="get"),
    path("logout/", LogoutView.as_view(), name="post"),
]
