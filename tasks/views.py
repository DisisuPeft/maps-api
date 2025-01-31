from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.authservice.authentication import ServiceJWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.


class TestApiView(APIView):
    authentication_classes = [ServiceJWTAuthentication]

    def get(self, request):
        user = request.user

        # Acceder a los atributos específicos
        user_data = {
            "id": user.id,
            "email": user.email,
            "roles": user.roles,  # El atributo que añadimos en el autenticador
            "is_staff": user.is_staff,
        }
        return Response(
            {"detail": "Service working", "user": user_data}, status=status.HTTP_200_OK
        )
