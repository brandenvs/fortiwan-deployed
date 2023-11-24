import requests, json, os
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required

app_name = 'fortiwan_config'

fortiwan_secret_token = os.environ.get('FORTIOS_REST_TOKEN')

app_label = 'fortiwan_config'

@login_required
def index(request):
    return render(request, 'fortiwan_config.html')

def put_interface(request):
    if request.method == "POST":
        ## [SETUP] ##
        session = requests.Session() # Provides cookie persistence, connection-pooling, and configuration.
        session.verify = False # Disable Verification
        session.trust_env = False # Prevent Tracking            
        print('name', request.POST.get('name'))
        print('interface', request.POST.get('interface'))

        return render(request, 'fortiwan_config.html')
    # 
    

    #     base_url = 'https://fortiwan.bcfa.co.za:444'
    #     api_secret = 'Ndfch8r79y86bn8ggGgc5Gf9pNb34z'      

    #     path = f'/vpn.ipsec/phase1-interface/{name}'

    #     url = f'{base_url}/{path}?access_token={api_secret}' # Build URL     
    #     method = 'POST' # Define Method
    #     data =
    #     failed = False # Flag
    #     headers = {'Content-Type': 'application/json'} # Define Headers


    #     # Make API POST
    #     try:
    #         response = session.get(url=url, headers=headers)
    #     except requests.exceptions.RequestException as e:
    #             print(f"Network Error: {e}")
    #             failed = True
    #     except json.JSONDecodeError as e:
    #             print(f"JSON Decode Error: {e}")
    #             failed = True
    #     except Exception as e:
    #             print(f"Unexpected Error: {e}")
    #             failed = True
        
    #     if failed != True:
    #         if response.status_code == 200:
    #             print(f'[SUCCESS] Received Response({response.status_code}) From - {base_url}/{vpn_ipsec}?<access_token>')
    #             try:
    #                 vpn_tunnels = response.json()
    #             except Exception as e:
    #                 print(f"Unexpected JSON Error: {e}")
    #         else:
    #             print(f'[ERROR] Received Response({response.status_code}) From - {base_url}/{vpn_ipsec}?<access_token>')
    #     else:
    #         print('[ERROR] Flag is TRUE!')
