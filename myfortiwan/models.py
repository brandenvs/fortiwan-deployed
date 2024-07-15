from django.db import models

class APIUser:
    def __init__(self, username, access_token, expires_in, token_type, scope, refresh_token, message, status):
        self.username = username
        self.access_token = access_token
        self.expires_is = expires_in
        self.token_type = token_type
        self.scope = scope
        self.refresh_token = refresh_token

# Firewall Model
class Firewall:
    def __init__(self, ip, name, comment, status, incoming_core, outgoing_core, incoming_tunnel, outgoing_tunnel, p2name, interface):
        self.ip = ip
        self.name = name        
        self.comment = comment
        self.status = status
        self.incoming_core = incoming_core
        self.outgoing_core = outgoing_core
        self.p2name = p2name
        self.incoming_tunnel = incoming_tunnel
        self.outgoing_tunnel = outgoing_tunnel
        self.interface = interface 