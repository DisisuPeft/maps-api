from django.db import models

# Create your models here.


class Profile(models.Model):
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.BigIntegerField()
    user = models.BigIntegerField()
