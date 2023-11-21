import requests, json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.http import JsonResponse
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers import serialize

fortiwan_secret_token = os.environ.get('FORTIOS_REST_TOKEN')

app_label = 'fortiwan_monitor'

# Session setup
session = requests.Session()
session.verify = False # Disable SSL Cert.
session.trust_env = False # Prevent tracking.

# Firewall object class
class Firewall:
    def __init__(self, ip, name, comment, status, incoming_core, outgoing_core, incoming_tunnel, outgoing_tunnel, p2name):
        self.ip = ip
        self.name = name        
        self.comment = comment
        self.status = status
        self.incoming_core = incoming_core
        self.outgoing_core = outgoing_core
        self.p2name = p2name
        self.incoming_tunnel = incoming_tunnel
        self.outgoing_tunnel = outgoing_tunnel

@login_required
def index(request):
    return render(request, 'fortiwan_monitor.html')

# Better ensure ajax & method should be GET.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

# [GET] IPsec VPN Tunnels
@login_required
def get_tunnels(request):
    filter_result = 'expire'
    if request.method == "GET":
        ## [SETUP] ##
        session = requests.Session() # Provides cookie persistence, connection-pooling, and configuration.
        session.verify = False # Disable Verification
        session.trust_env = False # Prevent Tracking

        base_url = 'https://fortiwan.bcfa.co.za:444'
        api_secret = settings.ACCESS_TOKEN      

        vpn_ipsec = 'api/v2/monitor/vpn/ipsec'

        request_api = f'{base_url}/{vpn_ipsec}/?access_token={api_secret}'                
                    
        failed = False # Flag        
         # Build Request URL
        headers = {'Content-Type': 'application/json'} # Define Headers
        # Make the API call & handle exceptions(if any)

        view_dict = {}
        firewalls = []

        try:
            response = session.get(url=request_api, headers=headers)
        except requests.exceptions.RequestException as e:
                print(f"Network Error: {e}")
                failed = True
        except json.JSONDecodeError as e:
                print(f"JSON Decode Error: {e}")
                failed = True
        except Exception as e:
                print(f"Unexpected Error: {e}")
                failed = True
        
        if failed != True:
            if response.status_code == 200:
                print(f'[SUCCESS] Received Response({response.status_code}) From - {base_url}/{vpn_ipsec}?<access_token>')
                try:
                    vpn_tunnels = response.json()
                except Exception as e:
                    print(f"Unexpected JSON Error: {e}")
            else:
                print(f'[ERROR] Received Response({response.status_code}) From - {base_url}/{vpn_ipsec}?<access_token>')
        else:
            print('[ERROR] Flag is TRUE!')
        
        # Deconstruct Initial JSON response
        vpn_tunnels = vpn_tunnels.get('results', [])
        
        
        for tunnel in vpn_tunnels:
            vpn_tunnel = tunnel.get('proxyid', [])
            if len(vpn_tunnel) > 0: # Check that the object has any vpn stats
                firewall_obj = Firewall(
                    ip=tunnel.get('tun_id'), 
                    name=tunnel.get('name'), 
                    comment=tunnel.get('comments'), 
                    status=vpn_tunnel[0]['status'], 
                    incoming_core=tunnel.get('incoming_bytes'), 
                    outgoing_core=tunnel.get('outgoing_bytes'),
                    p2name=vpn_tunnel[0]['p2name'],
                    incoming_tunnel=vpn_tunnel[0]['incoming_bytes'],
                    outgoing_tunnel=vpn_tunnel[0]['outgoing_bytes'])
                firewalls.append(firewall_obj)
        
    for firewall_obj in firewalls:
        #  print(firewall_obj)    
        view_dict.update({firewall_obj.name:{
            'ip': firewall_obj.ip, 
            'name': firewall_obj.name, 
            'comment': firewall_obj.comment, 
            'status': firewall_obj.status, 
            'incoming_core': firewall_obj.incoming_core, 
            'outgoing_core': firewall_obj.outgoing_core, 
            'p2name': firewall_obj.p2name, 
            'incoming_tunnel': firewall_obj.incoming_tunnel,
            'outgoing_tunnel': firewall_obj.outgoing_tunnel}})
    return JsonResponse(view_dict)
        