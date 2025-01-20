from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class HasRole(BasePermission):
    allowed_roles = []

    def __init__(self, allowed_roles=None):
        if allowed_roles is not None:
            self.allowed_roles = allowed_roles

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            raise PermissionDenied("El usuario no está autenticado.")

        if not user.rol.filter(name__in=self.allowed_roles).exists():
            raise PermissionDenied(f"El usuario no tiene los roles requeridos")

        return True


# Método de fábrica para definir roles dinámicos
def HasRoleWithRoles(allowed_roles):
    class CustomHasRole(HasRole):
        def __init__(self):
            super().__init__(allowed_roles=allowed_roles)

    return CustomHasRole
