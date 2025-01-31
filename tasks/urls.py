from django.contrib import admin
from django.urls import path, include
from tasks.views import TestApiView

urlpatterns = [
    # path("api/", include("autenticacion.urls")),
    path("endpoint/test/", TestApiView.as_view(), name="get")
]
