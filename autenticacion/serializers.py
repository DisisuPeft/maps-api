from autenticacion.models import UserCustomize, Roles, CustomPermission
from rest_framework import serializers
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import exceptions


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        credentials = {"email": attrs.get("email"), "password": attrs.get("password")}
        user = authenticate(**credentials)
        if user:
            if not user.is_active:
                raise exceptions.AuthenticationFailed("User is deactivated")


class PermissionCustomizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPermission
        fields = ["id", "name", "roles"]

        def create(self, validated_data):
            roles = validated_data.pop("roles", [])
            existing_roles = Roles.objects.filter(id__in=roles)
            if len(existing_roles) != len(roles):
                raise serializers.ValidationError("Uno o más roles no existen")
            try:
                with transaction.atomic():
                    permission = CustomPermission.objects.create(
                        name=validated_data["name"]
                    )
                    if roles:
                        permission.roles.add(*existing_roles)
                    permission.save()
                    return permission
            except Exception as e:
                raise serializers.ValidationError(
                    f"Error al crear el permiso: {str(e)}"
                )


class RoleCustomizeSerializer(serializers.ModelSerializer):
    permission = PermissionCustomizeSerializer(required=False)

    class Meta:
        model = Roles
        fields = ["id", "name", "permission"]

        def create(self, validated_data):
            role = Roles.objects.create(
                name=validated_data["name"],
            )
            role.save()
            return role


class UserCustomizeSerializer(serializers.ModelSerializer):
    # role_id = serializers.ListField(
    #     child=serializers.IntegerField(),
    #     required=False,
    #     allow_empty=True,
    # )
    rol = RoleCustomizeSerializer(many=True, required=False)
    email = serializers.CharField(
        required=True,
        error_messages={
            "blank": "El email del usuario no puede estar vacío.",
            "required": "El email del usuario es obligatorio.",
        },
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={
            "blank": "El campo contraseña no puede estar vacío.",
            "required": "La contraseña es obligatoria.",
        },
    )

    class Meta:
        model = UserCustomize
        fields = ["id", "email", "password", "rol"]

    def create(self, validated_data):
        role_ids = validated_data.pop("role", [])
        try:
            with transaction.atomic():

                user = UserCustomize.objects.create_user(**validated_data)
                if role_ids:
                    try:
                        roles = Roles.objects.filter(id__in=role_ids)
                        if len(roles) != len(role_ids):
                            raise serializers.ValidationError(
                                "Uno o más roles no existen"
                            )

                        # Agregar múltiples roles
                        user.rol.add(*roles)

                    except Roles.DoesNotExist:
                        raise serializers.ValidationError(
                            "Alguno de los roles especificados no existe"
                        )

                return user
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def validate_email(self, value):
        if UserCustomize.objects.filter(email=value).exists():
            raise serializers.ValidationError("El email ya se encuentra registrado")
        return value
