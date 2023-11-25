import requests, json
from django.conf import settings
from decouple import config, Csv
import os, time
from authentication.models import APIUser

# GET BEARER TOKEN
def get_token(request):
    """Obtain a Bearer Token for authenticated requests.

    This function sends a POST request to the Fortinet authentication API
    to retrieve a Bearer Token for subsequent authenticated API calls.

    :param request: The request object, typically from a Django web framework view.
                    It is used to check if the user is authenticated.
    
    :return: A Bearer Token string if authentication is successful, otherwise None.

    :raises: Exception if an unexpected error occurs during the API call."""
    if request.user.is_authenticated:
        api_user = APIUser.objects.filter(user=request.user) # NOTE Test Purposes
    
        # Get Last Issued Time
        issued_time = api_user.get().issued_time
        if issued_time > 0:
            compare_times = time.time() - issued_time
        print(compare_times)
        if compare_times < 3000:
            # Session Persists & Connection Pooling
            session = requests.Session() 
            # Session Verification & Tracking
            session.verify = True # Verification
            session.trust_env = False # Tracking

            # Base URL
            auth_url = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"

            # Payload Variables
            api_key = settings.API_KEY
            password = settings.PASSWORD
            client_id = settings.CLIENT_ID

            # print(f'{api_key} || {password} || {client_id}') NOTE TEST PURPOSES

            # Request Headers
            headers = {
                'Content-Type': 'application/json',
            }

            # Define Payload
            payload = {
                'username': api_key,
                'password': password,
                'client_id': client_id,
                'grant_type': 'password',
            }               
            
            api_user = None

            # Call API: POST
            try:
                response = session.request('post', auth_url, headers=headers, json=payload, verify=False)
                if response.status_code == 200:
                    print('[SUCCESS] Authorized User!', response.status_code)
                    # print(f'RESPONSE: {response.json()}') NOTE TEST PURPOSES                    
                    try:
                        # Create APIUser Object(for later usage...)
                        api_user = APIUser(
                            user = request.user, 
                            issued_time = time.time(),
                            access_token = response.json()['access_token'], 
                            expires_in = response.json()['expires_in'],
                            token_type = response.json()['token_type'],
                            scope = response.json()['scope'],
                            refresh_token = response.json()['refresh_token'],
                            message = response.json()['message'],
                            status = response.json()['status'])
                        # Extract
                    except Exception as e:
                        print('[ERROR] Could Not Extract a Bearer Token...', f'Unexpected Error: {e}')
            except Exception as e:
                print(f'Unexpected Error: {e}')
        if api_user:
            # Remove All API_users
            objects_to_remove = APIUser.objects.filter(user=request.user) # NOTE Test Purposes
            objects_to_remove.delete() # NOTE Test Purposes        
            # Save API Object to Database
            api_user.save()
            return api_user
        else:
            return '[Error] APIUser Object is Empty...'    
    else:
        api_user = APIUser.objects.filter(user=request.user) # NOTE Test Purposes
        return api_user
    # Update Environment Variable
    # if bearer_token:
    #     os.environ['BEARER_TOKEN'] = bearer_token

def api_call(request, sn, fos_api, payload):
    # Session Persists & Connection Pooling
    session = requests.Session() 
    # Session Verification & Tracking
    session.verify = True # Verification
    session.trust_env = False # Tracking
    
    # Define Region Base
    base_url = 'https://api.fortigate.forticloud.com/forticloudapi/v1/fgt'
    # Define Full Base
    api_url = f'{base_url}/{sn}/{fos_api}'

    response = None
    api_user = APIUser.objects.get(user=request.user) 

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_user.access_token}'
    }

    # Make API Request(GET)
    if request.method == 'GET':
        try:
            print(api_url)
            response = session.request('get', api_url, headers=headers, verify=False)
        except Exception as e:
            print(f'Unexpected Error: {e}')
    elif request.method == 'POST':
        try:
            response = session.request('post', api_url, headers=headers, json=payload, verify=False)
        except Exception as e:
            print(f'Unexpected Error: {e}')
    
    if response.status_code == 200:
        print('[SUCCESS] API Called!', response.status_code)
        return response
    else:
        print('[ERROR] Unable to Call API', response.status_code)
        return None

def get_tunnels(request):
    foc_api = 'api/v2/monitor/vpn/ipsec'
    sns = ['FGT60FTK2109D2Z2', 'FGT60FTK2109D2N4', 'FGT60FTK2109D33E', 'FGT60FTK23099VF4']

    tunnel_responses = []
    for sn in sns:
        # API Call Variables
        response = api_call(request, sn, foc_api, None)
        print(response.status_code)
        tunnel_responses.append(response.json())
    return tunnel_responses


   
    