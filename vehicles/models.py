from django.db import models


# Create your models here.
class Categorys(models.Model):
    name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TypeVehicle(models.Model):
    name = models.TextField()
    category = models.ForeignKey(Categorys, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Vehicle(models.Model):
    description = models.TextField()
    model_year = models.DateField(blank=True, null=True)
    vehicle_type = models.ForeignKey(TypeVehicle, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(
        Categorys, on_delete=models.SET_NULL, null=True
    )  # Añadí null=True ya que usas SET_NULL
    capacity = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# En el tema de el license plate va a ser una tabla aparte para que pueda contener
# informacion adicional
