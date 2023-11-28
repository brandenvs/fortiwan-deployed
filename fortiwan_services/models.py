from django.db import models

class IPsecVPN_1(models.Model):
    ip = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    comments = models.TextField()
    status = models.CharField(max_length=50)
    incoming_core = models.CharField(max_length=50)
    outgoing_core = models.CharField(max_length=50)
    p2name = models.CharField(max_length=50)
    incoming_tunnel = models.CharField(max_length=50)
    outgoing_tunnel = models.CharField(max_length=50)
    interface = models.CharField(max_length=50)

# Firewall Model
class IPsecVPN:
    def __init__(self, ip, name, comments, status, incoming_core, outgoing_core, incoming_tunnel, outgoing_tunnel, p2name, interface, src1, src2, src3, src4, dst1, dst2):
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
    
    def __str__(self):
        test_output = f'''-----------------------------------------------------------
IPsec/VPN Tunnel - {self.name} | {self.comments} | {self.ip}
STATUS: {self.status}
-----------------------------------------------------------
-- CLEAR TRAFFIC --
    Incoming: {self.incoming_core} MB/s
    Outgoing: {self.outgoing_core} MB/s
-- PROXIED TRAFFIC --
    Incoming: {self.incoming_tunnel} MB/s
    Outgoing: {self.outgoing_tunnel} MB/s
-----------------------------------------------------------
'''
        return test_output
