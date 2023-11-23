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

@login_required
def index(request):
    return render(request, 'fortiwan_monitor.html')

# [GET] IPsec VPN Tunnels
@login_required
def get_tunnels(request): # NOTE I must create a API CAll & POST function
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
        
        try:
            # Deconstruct Initial JSON response
            vpn_tunnels = vpn_tunnels.get('results', [])      
        except:
            return None

        for tunnel in vpn_tunnels:
            vpn_tunnel = tunnel.get('proxyid', [])
            if len(vpn_tunnel) > 0: # Check that the object has any vpn stats
                if tunnel.get('tun_id') == '41.198.140.97':
                     interface = get_interface(request)
                else:
                     interface = 'non'
                firewall_obj = Firewall(
                    ip=tunnel.get('tun_id'), 
                    name=tunnel.get('name'), 
                    comment=tunnel.get('comments'), 
                    status=vpn_tunnel[0]['status'], 
                    incoming_core=tunnel.get('incoming_bytes'), 
                    outgoing_core=tunnel.get('outgoing_bytes'),
                    p2name=vpn_tunnel[0]['p2name'],
                    incoming_tunnel=vpn_tunnel[0]['incoming_bytes'],
                    outgoing_tunnel=vpn_tunnel[0]['outgoing_bytes'],
                    interface=interface)
                firewalls.append(firewall_obj)
        
    for firewall_obj in firewalls: 
        view_dict.update({firewall_obj.name:{
            'ip': firewall_obj.ip, 
            'name': firewall_obj.name, 
            'comment': firewall_obj.comment, 
            'status': firewall_obj.status, 
            'incoming_core': round(firewall_obj.incoming_core / (1024.0 * 1024.0)), 
            'outgoing_core': round(firewall_obj.outgoing_core / (1024.0 * 1024.0)), 
            'p2name': firewall_obj.p2name, 
            'incoming_tunnel': round(firewall_obj.incoming_tunnel / (1024.0 * 1024.0)),
            'outgoing_tunnel': round(firewall_obj.outgoing_tunnel / (1024.0 * 1024.0)),
            'interface': firewall_obj.interface}})
    return JsonResponse(view_dict)

# NOTE Rebuild this!
def get_interface(request): # NOTE I must create a API CAll & POST function
        ## [SETUP] ## 
        session = requests.Session() # Provides cookie persistence, connection-pooling, and configuration.
        session.verify = False # Disable Verification
        session.trust_env = False # Prevent Tracking

        base_url = 'https://fortiwan.bcfa.co.za:444'
        api_secret = '--'     

        vpn_ipsec = f'api/v2/cmdb/vpn.ipsec/phase1-interface'

        request_api =  'https://fortiwanlm.bcfa.co.za:444/api/v2/cmdb/vpn.ipsec/phase1-interface/BCFA_Teraco?access_token=--' # f'{base_url}/{vpn_ipsec}/?access_token={api_secret}'                
                    
        failed = False # Flag        
         # Build Request URL
        headers = {'Content-Type': 'application/json'} # Define Headers
        # Make the API call & handle exceptions(if any)

        view_dict = {}
        vpn_interface = None

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
                print(f'[SUCCESS] Received Response({response.status_code}) From - {request_api}')
                try:
                    vpn_interface = response.json()
                except Exception as e:
                    print(f"Unexpected JSON Error: {e}")
            else:
                print(f'[ERROR] Received Response({response.status_code}) From - {request_api}')
        else:
            print('[ERROR] Flag is TRUE!')

        if vpn_interface: 
            # Deconstruct Initial JSON response
            try:
                vpn_interface = vpn_interface.get('results', [])         
                for interface in vpn_interface:          
                    wan_interface = interface.get('interface')
                    print(wan_interface)
                    if wan_interface == 'wan1':
                        wan_interface = 'MTN'
                    elif wan_interface == 'wan2':
                        wan_interface = 'ECHO'
                return str(wan_interface)
            except:
                 return 'no-interface'
        else:
             return 'no-interface'
             