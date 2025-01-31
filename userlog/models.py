from django.db import models
from userprofile.models import Profile

# Create your models here.


class UserLog(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    log = models.BigIntegerField()
    user = models.BigIntegerField()
