from django.db import models
from vehicles.models import Vehicle


# Create your models here.


class Plan(models.Model):
    name = models.CharField(max_length=255)
    total_estimated_distance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    total_estimated_time = models.TimeField(blank=True, null=True)
    total_actual_distance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    total_actual_time = models.TimeField(blank=True, null=True)
    total_stops = models.BigIntegerField()
    # puntuality = development
    # optimizacion_criteria = models.ForeignKey(Optimization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Task(models.Model):
    origin = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    destination = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    estimated_distance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    estimated_time = models.TimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    actual_time = models.TimeField(blank=True, null=True)
    actual_distance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    vehicles = models.ManyToManyField(Vehicle, related_name="vehicles")
    plans = models.ForeignKey(Plan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Optimization(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    response = models.JSONField()
    total_distance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    total_time = models.TimeField(null=True, blank=True)
    optimization_type = models.TextField()
    status = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comments(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Itinerary(models.Model):
    name = models.TextField()
    distance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    # traffic data
    time_estimed = models.TimeField(null=True, blank=True)
    tasks = models.ManyToManyField(Task, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
