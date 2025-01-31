from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import requests
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User


class ServiceJWTAuthentication:
    def authenticate(self, request):
        cookies = request.COOKIES
        if not cookies:
            return None
        try:
            user_data = self._get_user(cookies)
            user = self._convert_to_user(user_data)
            # print(user)
            return (user, None)
        except Exception as e:
            print("here")
            raise AuthenticationFailed(str(e))

    def authenticate_header(self, request):
        return "Cookie"

    def _get_user(self, cookies):
        response = requests.get(
            f"{settings.AUTH_SERVICE_URL}/api/auth/users/",
            cookies=cookies,
        )
        if response.status_code != 200:
            raise AuthenticationFailed("Invalid token or user not found")
        return response.json()

    def _convert_to_user(self, user_data):
        user_info = user_data.get("user", {})

        user = User()
        user.id = user_info.get("id")
        user.username = user_info.get("email")  # Usando email como username
        user.email = user_info.get("email")

        # Guardamos los roles como atributo adicional
        user.roles = user_info.get("rol", [])

        # Establecemos valores por defecto para campos requeridos
        user.is_active = True
        user.is_staff = any(role.get("name") == "Administrador" for role in user.roles)
        user.is_superuser = user.is_staff  # O ajusta según tu lógica
        user.first_name = ""
        user.last_name = ""

        # No guardar en la base de datos
        user._state.adding = False

        return user
