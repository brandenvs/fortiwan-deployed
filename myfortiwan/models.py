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