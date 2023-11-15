import subprocess, requests, json
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Tunnel
from django.utils import timezone
from fortiwan_monitor.views import get_tunnels

def index(request):
    ipsec_vpn_tunnels = get_tunnels(request)

    view_dict = {}    

    for tunnel_name, tunnel_value in ipsec_vpn_tunnels.items():
        tmp_dict = {}        
        tunnel_values = dict(tunnel_value)
        for key, value in tunnel_values.items():
            if key != 'proxyid':
                tmp_dict.update({key: value})
            else:     
                for proxy in value:
                    proxy_status = proxy['status']
                    proxy_expire = proxy['expire']
                    proxy_incoming_bytes = proxy['incoming_bytes']
                    proxy_outgoing_bytes = proxy['outgoing_bytes']
                    tmp_dict.update({'proxy_status': proxy_status})
                    tmp_dict.update({'proxy_expire': proxy_expire})
                    tmp_dict.update({'proxy_incoming_bytes': proxy_incoming_bytes})
                    tmp_dict.update({'proxy_outgoing_bytes': proxy_outgoing_bytes})
        view_dict.update({tunnel_name: tmp_dict})
    return render(request, 'fortiwan_dashboard.html', {'tunnels': view_dict}) 

