from django.db import models

class VPN_Tunnel(models.Model):
    name = models.CharField(max_length=255)
    connection_count = models.CharField(max_length=255) 
    comments = models.CharField(max_length=255)
    tun_id = models.CharField(max_length=255)   
    proxy_status = models.CharField(max_length=255)
    proxy_expire = models.CharField(max_length=255)
    proxy_outgoing_mb = models.CharField(max_length=255)
    proxy_incoming_mb = models.CharField(max_length=255)
    # timestamp = models.CharField(max_length=255)