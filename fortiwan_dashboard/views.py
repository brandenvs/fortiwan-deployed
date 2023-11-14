import subprocess, requests, json
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Tunnel
from django.utils import timezone

def fetch_tunnels(request):
    # Global variables
    base_url = 'https://fortiwan.bcfa.co.za:444' # (ORIGINAL REMOVED!)
    # API secret token
    api_secret = '?access_token=mH8HQ9kccjycm3tc6zbkQkjznmhb1x' # (ORIGINAL REMOVED!)

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
    # # [GET] VPN IPsec tunnel JSON objects
    # try:
    #     response_tunnels = session.get(request_api, headers=headers)                
    #     # Check for successful HTTP response (status code 200)
    #     if response_tunnels.status_code == 200:
    #         # Fetch IPsec tunnel JSON objects
    #         tunnel_objects = response_tunnels.json()
    #     else:
    #         print(f"HTTP Error: {response_tunnels.status_code}")

    # except requests.exceptions.RequestException as e:
    #     # Handle network-related/api-server errors
    #     print(f"Network Error: {e}")
    #     stop_it = True

    # except json.JSONDecodeError as e:
    #     # Handle JSON decoding errors
    #     print(f"JSON Decode Error: {e}")
    #     stop_it = True

    # except Exception as e:
    #     # Catch-all for other unexpected exceptions
    #     print(f"Unexpected Error: {e}")
    #     stop_it = True
    
    # while stop_it != True:
    #     proxy_ids = {}
    #     _results = tunnel_objects['results']
    #     # Loop through JSON Objects that resulted from the initial api request
    #     for _object in _results:
    #         # Locate Tunnel? Name & Proxyid JSON objects -> Reading/Updating dict data type with objects
    #         proxy_ids.update({_object['name']: _object['proxyid']})

    #     # Loop through dictionary used to store JSON objects & deconstruct further
    #     for name, json_object in proxy_ids.items():
    #         status = '--'
    #         download = 0
    #         upload = 0
    #         for json_fields in json_object:
    #             status = json_fields['status']
    #             download = json_fields['incoming_bytes']
    #             upload = json_fields['outgoing_bytes']

    #         timestamp = f'{timezone.now()}'          
    #         # Create a new Tunnel Object and save to database
    #         _tunnel = Tunnel(name=name, status=status, upload=upload, download=download, timestamp=timestamp)
    #         _tunnel.save()
    #     stop_it = True

    #     monitor_tunnels = Tunnel.objects.all()
    # return monitor_tunnels

def index(request):    
    return render(request, 'fortiwan_dashboard.html')    


