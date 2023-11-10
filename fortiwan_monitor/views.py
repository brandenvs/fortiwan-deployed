import requests, json
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Tunnel
from django.utils import timezone
from django.conf import settings

app_label = 'fortiwan_monitor'

def index(request):  
    return render(request, 'fortiwan_monitor.html')    


#### DEPRECATED CODE REMOVING...
    # Tunnel.objects.all().delete()
    # secret_host = 'https://fortiwan.bcfa.co.za:444'
    # secret_token = settings.FORTIWAN_SECRET_TOKEN

    # # Session setup
    # session = requests.Session()
    # session.verify = False # Disable the SSL Cert Check(This generates an SSL Cert warning!)
    # session.trust_env = False # Don't trust environment. Prevents tracking.

    # # FORTIOS - VPN (https://fndn.fortinet.net/index.php?/fortiapi/1-fortios/3139/1/vpn/)
    # # Flag
    # stop_it = False
    # # Setup
    # tunnels = []
    # vpn_ipsec = 'api/v2/monitor/vpn/ipsec'
    # request_api = f'{secret_host}/{vpn_ipsec}/{secret_token}'
    # headers = {'Content-Type': 'application/json'}

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

    #     myTunnels = Tunnel.objects.all()

        

