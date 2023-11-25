# IMPORTS
from django.db import models
from django.contrib.auth.models import User

class APIUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    issued_time = models.FloatField()
    access_token = models.CharField(max_length=255)
    expires_in = models.CharField(max_length=255)
    token_type = models.CharField(max_length=255)
    scope = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
