from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps
from django.contrib.auth.hashers import make_password


@receiver(post_migrate)
def create_default_data(sender, **kwargs):
    if sender.name == "autenticacion":
        UserCustomize = apps.get_model("autenticacion", "UserCustomize")
        Roles = apps.get_model("autenticacion", "Roles")

        try:
            # Crear rol si no existe
            role = Roles.objects.get_or_create(name="Administrador")[0]

            # Crear usuario si no existe
            if not UserCustomize.objects.filter(email="defp_99@hotmail.com").exists():
                # Primero creamos el usuario
                user = UserCustomize.objects.create(
                    email="defp_99@hotmail.com",
                    password=make_password("daniel123"),
                )
                # Luego asignamos los roles usando el método add()
                user.rol.add(role)
                print("Usuario administrador creado exitosamente")
        except Exception as e:
            print(f"Error creando datos por defecto: {e}")
