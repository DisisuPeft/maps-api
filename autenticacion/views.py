from django.shortcuts import render
from contextvars import Token
from django.db import models
from autenticacion.manager import CustomUserManager
from autenticacion.models import UserCustomize as User
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from autenticacion.serializers import UserCustomizeSerializer
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.conf import settings
from rest_framework.views import APIView
from .authenticate import CustomJWTAuthentication


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if request.data["password"] != request.data["password_confirmation"]:
            return Response(
                {"error": "Las password no coinciden"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_serializer = UserCustomizeSerializer()
        user = user_serializer.create(request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(
                {"message": "Usuario creado con exito"}, status=status.HTTP_200_OK
            )
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                access_token = response.data.get("access")
                refresh_token = response.data.get("refresh")
                response.set_cookie(
                    "access",
                    access_token,
                    max_age=settings.AUTH_COOKIE_MAX_AGE,
                    path=settings.AUTH_COOKIE_PATH,
                    secure=settings.AUTH_COOKIE_SECURE,
                    httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                    samesite=settings.AUTH_COOKIE_SAMESITE,
                )
                response.set_cookie(
                    "refresh",
                    refresh_token,
                    max_age=settings.AUTH_COOKIE_MAX_AGE,
                    path=settings.AUTH_COOKIE_PATH,
                    secure=settings.AUTH_COOKIE_SECURE,
                    httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                    samesite=settings.AUTH_COOKIE_SAMESITE,
                )
                # response.data.pop("access", None)
                # response.data.pop("refresh", None)
            else:
                if response.status_code == status.HTTP_401_UNAUTHORIZED:
                    response.data = {
                        "error": "Por favor, verifique su email y contraseña."
                    }
                elif response.status_code == status.HTTP_400_BAD_REQUEST:
                    response.data = {
                        "error": "Se produjo un error en la solicitud. Por favor, revise los datos enviados."
                    }
            return response
        except Exception as e:
            print(f"Excepción capturada: {e}")
            return Response(
                {
                    "error": "Ocurrió un error al autenticar el usuario, verifica tu informacion"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")

        if refresh_token:
            request.data["refresh"] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get("access")

            response.set_cookie(
                "access",
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )

        return response


class CustomTokenVerifyView(TokenVerifyView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get("access")

        if access_token:
            request.data["token"] = access_token

        return super().post(request, *args, **kwargs)


class CheckUser(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request, *args, **kwargs):
        auth = request.user
        if hasattr(User, "rol") and isinstance(User.rol.field, models.ManyToManyField):
            user = User.objects.prefetch_related("rol").get(email=auth)
        else:
            user = User.objects.select_related("rol").get(email=auth)

        serializer = UserCustomizeSerializer(user)
        # print(user)
        if auth.is_authenticated:
            return Response(
                {"is_auth": True, "user": serializer.data}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Usuario no autenticado"}, status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access")
        response.delete_cookie("refresh")

        return response
