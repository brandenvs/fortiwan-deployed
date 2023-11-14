import requests, json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.http import JsonResponse
import os

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
   # Global variables
    base_url = 'https://fortiwan.bcfa.co.za:444' # (ORIGINAL REMOVED!)
    # API secret token
    api_secret = f'?access_token=mH8HQ9kccjycm3tc6zbkQkjznmhb1x' # (ORIGINAL REMOVED!)

    test_return = {}
    # Session setup
    session = requests.Session()
    session.verify = False # Disable the SSL Cert Check(This generates an SSL Cert warning!)
    session.trust_env = False # Don't trust environment. Prevents tracking.

    # FORTIOS - VPN (https://fndn.fortinet.net/index.php?/fortiapi/1-fortios/3139/1/vpn/)
    # Flag
    stop_it = False
    # Setup
    tunnels = []
    vpn_ipsec = 'api/v2/monitor/vpn/ipsec'
    request_api = f'{base_url}/{vpn_ipsec}/{api_secret}'
    headers = {'Content-Type': 'application/json'}
    if not stop_it:  # Continue if stop_it is False
        try:
            response_tunnels = session.get(request_api, headers=headers)
            if response_tunnels.status_code == 200:
                tunnel_objects = response_tunnels.json()
            else:
                print(f"HTTP Error: {response_tunnels.status_code}")
                stop_it = True

        except requests.exceptions.RequestException as e:
            print(f"Network Error: {e}")
            stop_it = True

        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            stop_it = True

        except Exception as e:
            print(f"Unexpected Error: {e}")
            stop_it = True

        if not stop_it:  # Continue if stop_it is still False
            proxy_ids = {}
            name = ''
            _results = tunnel_objects.get('results', [])
            for _object in _results:
                proxy_ids.update({_object.get('name'): _object.get('proxyid', [])})
                name = _object.get('name')

            for name, json_object in proxy_ids.items():
                status = '--'
                for json_fields in json_object:
                    status = json_fields.get('status', '--')
                test_return.update({ name: status })
    return JsonResponse(test_return)