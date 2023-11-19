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
from .models import VPN_Tunnel

fortiwan_secret_token = os.environ.get('FORTIOS_REST_TOKEN')

app_label = 'fortiwan_monitor'

# Session setup
session = requests.Session()
session.verify = False # Disable SSL Cert.
session.trust_env = False # Prevent tracking.

@login_required
def index(request):
    return render(request, 'fortiwan_monitor.html')

# Better ensure ajax & method should be GET.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

# [GET] IPsec VPN Tunnels
@login_required
def get_tunnels(request):
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
                    vpn_tunnels = response.json()
                except Exception as e:
                    print(f"Unexpected JSON Error: {e}")
            else:
                print(f'[ERROR] Received Response({response.status_code}) From - {base_url}/{vpn_ipsec}<access_token?>')
        else:
            print('[ERROR] Flag is TRUE!')
        # Deconstruct Initial JSON response
        vpn_tunnels = vpn_tunnels.get('results', [])

        tunnel_dict = {}
        for tunnel in vpn_tunnels:
            proxy_objects = tunnel.get('proxyid', [])
            if len(proxy_objects) > 0: # Check that the object has any vpn stats
                tunnel_dict.update({tunnel.get('name'): tunnel})
            else:
                continue
        
        view_dict = {} 

        for tunnel_name, tunnel_value in tunnel_dict.items():
            tmp_dict = {}
            try:      
                tunnel_values = dict(tunnel_value)
            except:
                break
            for key, value in tunnel_values.items():
                if key != 'proxyid':
                    tmp_dict.update({key: value})
                else:     
                    for proxy in value:
                        proxy_status = proxy['status']
                        proxy_expire = proxy['expire']
                        proxy_incoming_bytes = proxy['incoming_bytes']
                        proxy_incoming_mb = proxy_incoming_bytes / (1024 * 1024)
                        proxy_outgoing_bytes = proxy['outgoing_bytes']
                        proxy_outgoing_mb = proxy_outgoing_bytes / (1024 * 1024)
                        tmp_dict.update({'proxy_status': proxy_status})
                        tmp_dict.update({'proxy_expire': proxy_expire})
                        tmp_dict.update({'proxy_incoming_mb': round(proxy_incoming_mb)})
                        tmp_dict.update({'proxy_outgoing_mb': round(proxy_outgoing_mb)})
            view_dict.update({tunnel_name: tmp_dict})         
        # save_tunnels(request, view_dict)              
        return JsonResponse(view_dict)
    else:
        return HttpResponse("Forbidden!")

def save_tunnels(request, data):
    all_data = VPN_Tunnel.objects.all().delete()    
    count = 0
    for tunnel in data.values():
        print(tunnel['name'])
        count += 1
        name = tunnel['name'],
        connection_count = tunnel['connection_count'],
        comments = tunnel['comments'],
        tun_id = tunnel['tun_id'],
        proxy_status = tunnel['proxy_status'],
        proxy_expire = tunnel['proxy_expire'],
        proxy_outgoing_mb = tunnel['proxy_outgoing_mb'],
        proxy_incoming_mb = tunnel['proxy_incoming_mb'],
        save_tunnel = VPN_Tunnel(count, name, connection_count, comments, tun_id, proxy_status, proxy_expire, proxy_outgoing_mb, proxy_incoming_mb)
        save_tunnel.save()
