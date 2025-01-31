from django.conf import settings
import requests
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse
from rest_framework import status


class ServiceAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.auth_service_url = settings.AUTH_SERVICE_URL

    def __call__(self, request):
        # Realiza una condiciion para excluir rutas no necesarias
        # Obtiene el token del request, si no hay token indica que no fue proveido.
        # de lo contrario realiza la peticion a la ruta verify del serivicio
        # si no es valido devuelve un 401
        # si es valido, solo retorna el siguiente request
        # si no se cumple el "intenta" devuelve que hay una excepcion y el error
        try:
            cookies = request.COOKIES
            # print(auth_header)
            access_token = cookies.get("access")

            if not access_token:
                # print(request.META)
                raise AuthenticationFailed("No authentication token provided")
            # cut = auth_header.split(";")
            is_valid = self._verify_token_with_auth_service(access_token)
            # print(is_valid)
            if not is_valid:
                # print(is_valid)
                return JsonResponse(
                    {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
                )
            return self.get_response(request)
        except Exception as e:
            # print("here")
            return JsonResponse({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

    # funcion que hace la peticion al servicio. el AUTH_SERVICE_URL es un valor de .env
    def _verify_token_with_auth_service(self, token):
        # print(auth_header[0].split("="), auth_header[1].split("="))
        # access = auth_header[0].split("=")
        # refresh = auth_header[1].split("=")
        # print(token)
        try:
            response = requests.post(
                f"{self.auth_service_url}/api/auth/verify/",
                cookies={"access": token},
            )
            # print(*response)
            return response.status_code == 200
        except requests.RequestException:
            raise AuthenticationFailed("Authentication service unvailable")
