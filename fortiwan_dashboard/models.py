from django.db import models


class Tunnel(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    upload = models.CharField(max_length=255)
    download = models.CharField(max_length=255)
    timestamp = models.CharField(max_length=255)