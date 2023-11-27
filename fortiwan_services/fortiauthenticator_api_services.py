import requests, time
from django.conf import settings
from authentication.models import APIUser

# Check for API User
def get_apiuser(request):
    no_api_user = False
    try:
        api_user = APIUser.objects.filter(user=request.user)
        if api_user.get().user.username == None:
            no_api_user = True
    except Exception as e:
        no_api_user = True
    
    if no_api_user:
        print(f'[OPERATION-REQUIRED] No API User Found for: {request.user.username}...\n')
        return 404
    
    print('[SUCCESS] Found API User!--USERNAME: ', api_user.get().user.username, end='\n')
    return api_user

# Check if Token has Expired
def has_expired(api_user):
    existed_for = time.time() - api_user.get().issued_time        
    if existed_for >= 3700:
        print('[OPERATION-REQUIRED] Your Bearer Token has Expired-- Do not worry!\nATTEMPTING REFRESHING OF BEARER TOKEN...\n')
        return True
    else:
        print('[SUCCESS] Current API User Bearer Token is VALID!')
        return False

# Call FortiAuthenticator to Refresh API User's Token
def refresh_token(api_user):
    # Get API User Refresher Token from Db
    refresh_token = api_user.get().refresh_token

    # Define FortiAuthentication API Call
    auth_url = "https://customerapiauth.fortinet.com/api/v1/oauth/token/" # [auth_URL]

    # Define Request Headers
    headers = {
        'Content-Type': 'application/json',
    }

    # Define JSON Payload
    payload = {            
        'client_id': settings.CLIENT_ID,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    session = requests.Session() # Provides cookie persistence, connection-pooling, and configuration.
    session.verify = False # Disable Verification
    session.trust_env = False # Prevent Tracking
    
    # Setup Session
    # Calls FortiAuthenticator API POST Request        
    try:
        response_refresh = session.request('post', auth_url, headers=headers, json=payload, verify=False)
        if response_refresh.status_code == 200:
            print('[SUCCESS] FortiAuthenticator Issued a API User Refreshed Bearer Token!\n--', f'RESPONSE STATUS CODE: {response_refresh.status_code}')
        else:
            print(f'[ERROR] FortiAuthenticator was Unable to Refresh API User Bearer Token...\nRESPONSE STATUS CODE: {response_refresh.status_code}')
    except Exception as e:
        print(f'[ERROR] FortiAuthenticator was Unable to Refresh API User Bearer Token...\nPYTHON EXCEPTION: {e}\n\nRESPONSE STATUS CODE: {response_refresh.status_code}')

# GET BEARER TOKEN
def get_token(request):
    """Obtain a Bearer Token for authenticated requests.

    This function sends a POST request to the Fortinet authentication API
    to retrieve a Bearer Token for subsequent authenticated API calls.

    :param request: The request object, typically from a Django web framework view.
                    It is used to check if the user is authenticated.
    
    :return: A Bearer Token string if authentication is successful, otherwise None.

    :raises: Exception if an unexpected error occurs during the API call."""
    # Check for API User
    api_user = get_apiuser(request)

    if api_user != 404:
        # Check API User Bearer Token Expiry
        expired = has_expired(api_user)
        # IF Token Expired attempt Refresh
        if expired:



    # Flags
    stop_flag = False
    out_of_time = False
    no_api_user = False
    print('[ERROR] Standard User Must be Logged In to Preform this Task...')
    

    # Base URL
    auth_url = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"

    # Payload Variables    
    api_key = settings.API_KEY
    password = settings.PASSWORD

    # Define Headers
    headers = {
        'Content-Type': 'application/json',
    }    
    
    # API User
    api_user = None
    
   

    # FortiAuthorizer Issues a Refreshed Bearer Token
    if out_of_time and api_user:
        local_flag = False
        print('REFRESH TOKEN: ', api_user.get().refresh_token)
        refresh_token = api_user.get().refresh_token
        # Redefine Request Headers
        headers = {
            'Content-Type': 'application/json',
        }    
        payload = {            
            'client_id': client_id,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        # Redefine Base URL
        auth_url = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"
        # Calls FortiAuthenticator API POST Request        
        try:
            response_refresh = session.request('post', auth_url, headers=headers, json=payload, verify=False)
            if response_refresh.status_code == 200:
                print('[SUCCESS] FortiAuthenticator Issued a API User Refreshed Bearer Token!\n--', f'RESPONSE STATUS CODE: {response_refresh.status_code}')
            else:
                print(f'[ERROR] FortiAuthenticator was Unable to Refresh API User Bearer Token...\nRESPONSE STATUS CODE: {response_refresh.status_code}')
                local_flag = True
        except Exception as e:
            print(f'[ERROR] FortiAuthenticator was Unable to Refresh API User Bearer Token...\nPYTHON EXCEPTION: {e}\n\nRESPONSE STATUS CODE: {response_refresh.status_code}')
            local_flag = True
        
        if local_flag:
            return None

    # FortiAuthorizer Issues a NEW Bearer Token
    if no_api_user:
        # Define Payload
        payload = {
            'username': api_key,
            'password': password,
            'client_id': client_id,
            'grant_type': 'password',
        }
        # Calls FortiAuthenticator API POST Request        
        try:
            new_response = session.request('post', auth_url, headers=headers, json=payload, verify=False)
            if new_response.status_code != 200:
                print(f'[ERROR] FortiAuthenticator was unable to login user...\nSTATUS CODE: {new_response.status_code}')
                stop_flag = True
            else:
                print('[SUCCESS] Authorized User!', new_response.status_code)
        except Exception as e:
            print(f'[ERROR] FortiAuthenticator was unable to login user...\nUnexpected Error: {e}')
            stop_flag = True
        
        # Create API User Object
        api_user = APIUser(
            user = request.user, 
            issued_time = time.time(),
            access_token = new_response.json()['access_token'], 
            expires_in = new_response.json()['expires_in'],
            token_type = new_response.json()['token_type'],
            scope = new_response.json()['scope'],
            refresh_token = new_response.json()['refresh_token'],
            message = new_response.json()['message'],
            status = new_response.json()['status'])
        
        # Check for Already existing API User against current user(desired: no api user object present!)
        objects_to_remove = APIUser.objects.filter(user=request.user) # NOTE Test Purposes
        objects_to_remove.delete()

        # Save API Object to Database
        api_user.save()
        print('[SUCCESS] Created API User!')

    # Check for Stop Flag
    if stop_flag:
        print('[ERROR] STOP FLAG IS:', stop_flag)
        return None
    
    # Create API User & Save Object to Database
    if no_api_user:
        
        return api_user
    elif api_user and out_of_time:
        # Update User
        update_api_user = APIUser.objects.filter(user=request.user)[0]
        print(update_api_user.user.username, response_refresh.text)
        
        update_api_user.access_token = response_refresh.json()['access_token']
        update_api_user.refresh_token = response_refresh.json()['refresh_token']
        update_api_user.message = response_refresh.json()['message']
        update_api_user.save()        
        return api_user
    # If All Fails(IAF)... Print & Return None
    print('[ERROR] Unknown IAF Error at "get_token()" Function...')
    return None

def api_call(request, sn, fos_api, payload):
    """Make an API call to the FortiCloud API.

    This function performs either a GET or POST request to the FortiCloud API
    based on the provided HTTP request method. It utilizes a session with
    connection pooling and persists a Bearer Token for authentication.

    :param request: The HTTP request object, typically from a Django web framework view.
    :param sn: The serial number of the FortiGate device.
    :param fos_api: The specific FortiCloud API endpoint.
    :param payload: The payload to be included in the request for POST method.

    :return: The response object if the API call is successful (status code 200),
             otherwise None.

    :raises: Exception if an unexpected error occurs during the API call.
    """
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
    get_token(request)
    # foc_api = 'api/v2/monitor/vpn/ipsec'
    # sns = ['FGT60FTK2109D2Z2', 'FGT60FTK2109D2N4', 'FGT60FTK2109D33E', 'FGT60FTK23099VF4']

    # tunnel_responses = []
    # for sn in sns:
    #     # API Call Variables
    #     response = api_call(request, sn, foc_api, None)
    #     print(response.status_code)
    #     tunnel_responses.append(response.json())
    # return tunnel_responses


   
    