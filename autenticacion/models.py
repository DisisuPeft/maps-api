from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.fields.related import ForeignKey
from autenticacion.manager import CustomUserManager


# Create your models here.
class Roles(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class CustomPermission(models.Model):
    name = models.CharField(max_length=100)
    roles = models.ManyToManyField(Roles, related_name="custom_permissions")

    def __str__(self):
        return self.name


class UserCustomize(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    rol = models.ManyToManyField(Roles, related_name="user_customize")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def has_permission(self, permission_id):
        return self.rol.filter(custom_permissions__id=permission_id)

    def __str__(self):
        return self.email
