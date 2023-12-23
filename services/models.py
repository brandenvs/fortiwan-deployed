from django.db import models
from django.contrib.auth.models import User

# API User Model
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

# Site View Model
class Site:
    def __init__(self, ip, name, comments, status, incoming_core, outgoing_core, incoming_tunnel, outgoing_tunnel, p2name, interface, src1, src2, src3, src4, dst1, dst2, serial_number):
        self.ip = ip
        self.name = name        
        self.comments = comments
        self.status = status
        self.incoming_core = incoming_core
        self.outgoing_core = outgoing_core
        self.p2name = p2name
        self.incoming_tunnel = incoming_tunnel
        self.outgoing_tunnel = outgoing_tunnel
        self.interface = interface
        
        self.src1 = src1
        self.src2 = src2
        self.src3 = src3
        self.src4 = src4

        self.dst1 = dst1
        self.dst2 = dst2
        
        self.serial_number = serial_number

    def update_interface(self, new_interface):
        self.interface = new_interface
    
    def get_serial_number(self):
        return self.serial_number
    
    def __str__(self):
        test_output = f'''------------------------------------------------------------------------
IPsec/VPN Tunnel - {self.name} | {self.comments} | {self.ip}
STATUS: {self.status}
-----------------------------
-- CLEAR TRAFFIC --
    Incoming: {self.incoming_core} MB/s
    Outgoing: {self.outgoing_core} MB/s
-- PROXIED TRAFFIC --
    Incoming: {self.incoming_tunnel} MB/s
    Outgoing: {self.outgoing_tunnel} MB/s
-- INTERFACE --
    {self.interface}'''
        return test_output
    
