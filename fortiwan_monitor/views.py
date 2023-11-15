import requests, json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.http import JsonResponse
import os
from django.conf import settings

fortiwan_secret_token = os.environ.get('FORTIOS_REST_TOKEN')

app_label = 'fortiwan_monitor'

# Session setup
session = requests.Session()
session.verify = False # Disable SSL Cert.
session.trust_env = False # Prevent tracking.

def index(request):
    return render(request, 'fortiwan_monitor.html')

# [GET] IPsec VPN Tunnels
def get_tunnels(request):
    if request.user.is_authenticated:
        ## [SETUP] ##
        session = requests.Session() # Provides cookie persistence, connection-pooling, and configuration.
        session.verify = False # Disable Verification
        session.trust_env = False # Prevent Tracking

        base_url = 'https://fortiwan.bcfa.co.za:444'
        api_secret = settings.ACCESS_TOKEN

        failed = False # Flag
        vpn_ipsec = 'api/v2/monitor/vpn/ipsec' # Area of API
        request_api = f'{base_url}/{vpn_ipsec}/?access_token={api_secret}' # Build Request URL
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
                print(f'[SUCCESS] Received Response({response.status_code}) From - {base_url}/{vpn_ipsec}<access_token?>')
                try:
                    vpn_tunnels = response.json()
                except Exception as e:
                    print(f"Unexpected JSON Error: {e}")
            else:
                print(f'[ERROR] Received Response({response.status_code}) From - {base_url}/{vpn_ipsec}<access_token?>')
        else:
            print('[ERROR] Flag is TRUE!')

        # Deconstruct JSON response
        vpn_tunnels = vpn_tunnels.get('results', [])

        tunnel_dict = {}
        for tunnel in vpn_tunnels:
            proxy_objects = tunnel.get('proxyid', [])
            if len(proxy_objects) > 0: # Check that the object has any vpn stats
                tunnel_dict.update({tunnel.get('name'): tunnel})
            else:
                 continue
        return tunnel_dict
    else:
        return HttpResponse("Forbidden!")