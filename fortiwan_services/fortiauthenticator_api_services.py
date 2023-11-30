import requests, time
from django.conf import settings
from authentication.models import APIUser
from . import models as vmc
from django.core.serializers import serialize
from django.http import JsonResponse

'''rollback code
# # Check for API User
# def get_apiuser(request):
#     no_api_user = False
#     try:
#         api_user = APIUser.objects.filter(user=request.user)
#         if api_user.get().user.username == None:
#             no_api_user = True
#     except Exception as e:
#         no_api_user = True
    
#     if no_api_user:
#         print(f'[OPERATION-REQUIRED] No API User Found for: {request.user.username}...\n')
#         return 404
    
#     print('[SUCCESS] Found API User!--USERNAME: ', api_user.get().user.username, end='\n')
#     return api_user
'''
def get_apiuser(request):
    """
    Get the API user associated with the given request.

    This function checks for the existence of an APIUser associated with the
    provided Django HTTP request object. If no APIUser is found or an exception
    occurs during the check, it returns a 404 status.

    :param request: Django HTTP request object.

    :return: APIUser object if found, otherwise 404 status.

    Example Usage:
    ```
    request = get_authenticated_request()  # Replace with actual authentication logic
    api_user = get_apiuser(request)
    if api_user != 404:
        print(f"API User found! Username: {api_user.user.username}")
    else:
        print("No API User found.")
    ```
    """

    no_api_user = False

    try:
        # Attempt to retrieve APIUser associated with the user in the request
        api_user = APIUser.objects.get(user=request.user)

        # Check if the username is None
        if api_user.user.username is None:
            no_api_user = True

    except APIUser.DoesNotExist:
        # APIUser not found
        no_api_user = True

    except Exception as e:
        # Other unexpected errors
        no_api_user = True

    if no_api_user:
        # Log a message and return 404 status if no APIUser is found
        print(f'[OPERATION-REQUIRED] No API User Found for: {request.user.username}...\n')
        return 404

    # Log success and return the APIUser object
    print('[SUCCESS] Found API User! -- USERNAME:', api_user.user.username, end='\n')
    return api_user

'''rollback code
# # Check if Token has Expired
# def has_expired(api_user):
#     existed_for = time.time() - api_user.get().issued_time        
#     if existed_for >= 3700:
#         print('[OPERATION-REQUIRED] Your Bearer Token has Expired-- Do not worry!\nATTEMPTING REFRESHING OF BEARER TOKEN...\n')
#         return True
#     else:
#         print('[SUCCESS] Current API User Bearer Token is VALID!')
#         return False
'''
def has_expired(api_user):
    """
    Check if the Bearer Token associated with the given APIUser has expired.

    This function calculates the duration since the Bearer Token was issued
    and checks if it has been longer than the threshold (3700 seconds). If
    the token has expired, it prints a message indicating the need for
    refreshing and returns True. Otherwise, it prints a success message
    and returns False.

    :param api_user: APIUser object.

    :return: True if the Bearer Token has expired, False otherwise.

    Example Usage:
    ```
    api_user = get_apiuser(request)
    if api_user != 404:
        if has_expired(api_user):
            print("Bearer Token needs refreshing.")
        else:
            print("Bearer Token is still valid.")
    else:
        print("No API User found.")
    ```
    """

    # Calculate the duration since the Bearer Token was issued
    existed_for = time.time() - api_user.issued_time

    if existed_for >= 3700:
        # Token has expired
        print('[OPERATION-REQUIRED] Your Bearer Token has Expired -- Do not worry!\nATTEMPTING REFRESHING OF BEARER TOKEN...\n')
        return True
    else:
        # Token is still valid
        print('[SUCCESS] Current API User Bearer Token is VALID!')
        return False

'''rollback code
# # Call FortiAuthenticator to Refresh API User's Token
# def refresh_token(api_user):
#     # Get API User Refresher Token from Db
#     refresh_token = api_user.get().refresh_token

#     # Define Auth URL
#     auth_url = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"

#     # Define Request Headers
#     headers = {
#         'Content-Type': 'application/json',
#     }

#     # Define JSON Payload
#     payload = {            
#         'client_id': settings.CLIENT_ID,
#         'grant_type': 'refresh_token',
#         'refresh_token': refresh_token
#     }

#     # Setup Session
#     session = requests.Session() # Provides Connection Pooling Persistence
#     session.verify = False # Disable Verification
#     session.trust_env = False # Prevent Tracking

#     try:
#         # Make a (Refresher) FortiAuthenticator Request
#         response = session.request('post', auth_url, headers=headers, json=payload, verify=False) # NOTE VERIFY SHOULD BE TRUE
#         if response.status_code == 200:
#             print('[SUCCESS] FortiAuthenticator Issued a API User Refreshed Bearer Token!-- ', f'RESPONSE STATUS CODE: {response.status_code}\n')
#             return response
#         else:
#             print('[ERROR] FortiAuthenticator was Unable to Refresh API User Bearer Token-- ', f'RESPONSE STATUS CODE: {response.status_code}\n')
#             return response
#     except Exception as e:
#         print(f'[ERROR] FortiAuthenticator was Unable to Refresh API User Bearer Token...\n{e}\n')
#         return 404
'''
def refresh_token(api_user):
    """
    Refresh the API User's Bearer Token by making a request to FortiAuthenticator.

    This function uses the refresh token stored in the APIUser object to obtain
    a new Bearer Token from FortiAuthenticator. It returns the response object
    if the refresh is successful, otherwise it returns the response object
    with an error message.

    :param api_user: APIUser object.

    :return: Response object if the refresh is successful, 404 status otherwise.

    Example Usage:
    ```
    api_user = get_apiuser(request)
    if api_user != 404:
        response = refresh_token(api_user)
        if response and response.status_code == 200:
            print("Bearer Token refreshed successfully.")
        else:
            print("Error refreshing Bearer Token.")
    else:
        print("No API User found.")
    ```
    """

    # Get API User Refresher Token from Db
    refresh_token = api_user.refresh_token

    # Define Auth URL
    auth_url = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"

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

    # Setup Session
    session = requests.Session()  # Provides Connection Pooling Persistence
    session.verify = False  # Disable Verification
    session.trust_env = False  # Prevent Tracking

    try:
        # Make a (Refresher) FortiAuthenticator Request
        response = session.post(auth_url, headers=headers, json=payload, verify=False)  # NOTE VERIFY SHOULD BE TRUE
        if response.status_code == 200:
            print('[SUCCESS] FortiAuthenticator Issued a API User Refreshed Bearer Token!-- ', f'RESPONSE STATUS CODE: {response.status_code}\n')
        else:
            print('[ERROR] FortiAuthenticator was Unable to Refresh API User Bearer Token-- ', f'RESPONSE STATUS CODE: {response.status_code}\n')
        return response

    except Exception as e:
        print(f'[ERROR] FortiAuthenticator was Unable to Refresh API User Bearer Token...\n{e}\n')
        return 404

'''rollback code
# # Create a NEW API User object
# def auth_credentials():
#     # Define Auth URL
#     auth_url = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"

#     # Define Request Headers
#     headers = {
#         'Content-Type': 'application/json',
#     }

#     # Define JSON Payload
#     payload = {
#         'username': settings.API_KEY,
#         'password': settings.PASSWORD,
#         'client_id': settings.CLIENT_ID,
#         'grant_type': 'password',
#     }

#     # Setup Session
#     session = requests.Session() # Provides Connection Pooling Persistence
#     session.verify = False # Disable Verification
#     session.trust_env = False # Prevent Tracking

#      # Calls FortiAuthenticator API POST Request        
#     try:
#         response = session.request('post', auth_url, headers=headers, json=payload, verify=False)
#         if response.status_code == 200:
#             print('[SUCCESS] FortiAuthenticator Authorized Bearer & Refresher Tokens-- ', response.status_code, end='\n')
#             return response
#         else:
#             print('[ERROR] FortiAuthenticator was Unable to Authorize Bearer & Refresher Tokens-- ', {response.status_code}, end='\n')
#             return response.status_code
#     except Exception as e:
#         print(f'[ERROR] FortiAuthenticator Unable to Authenticate User Credentials...\nUnexpected Error: {e}\n')
#         return 404
'''
def auth_credentials():
    """
    Authenticate credentials with FortiAuthenticator to obtain Bearer and Refresher Tokens.

    This function sends a POST request to FortiAuthenticator with the provided
    API credentials (API_KEY, PASSWORD, CLIENT_ID) to obtain Bearer and Refresher Tokens.
    It returns the response object if the authentication is successful,
    otherwise it returns the HTTP status code.

    :return: Response object if the authentication is successful, HTTP status code otherwise.

    Example Usage:
    ```
    response = auth_credentials()
    if response and response.status_code == 200:
        print("Authentication successful. Bearer and Refresher Tokens obtained.")
    else:
        print("Error authenticating credentials.")
    ```
    """

    # Define Auth URL
    auth_url = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"

    # Define Request Headers
    headers = {
        'Content-Type': 'application/json',
    }

    # Define JSON Payload
    payload = {
        'username': settings.API_KEY,
        'password': settings.PASSWORD,
        'client_id': settings.CLIENT_ID,
        'grant_type': 'password',
    }

    # Setup Session
    session = requests.Session()  # Provides Connection Pooling Persistence
    session.verify = False  # Disable Verification
    session.trust_env = False  # Prevent Tracking

    # Calls FortiAuthenticator API POST Request
    try:
        response = session.post(auth_url, headers=headers, json=payload, verify=False)
        if response.status_code == 200:
            print('[SUCCESS] FortiAuthenticator Authorized Bearer & Refresher Tokens -- ', response.status_code, end='\n')
        else:
            print('[ERROR] FortiAuthenticator was Unable to Authorize Bearer & Refresher Tokens -- ', {response.status_code}, end='\n')
        return response

    except Exception as e:
        print(f'[ERROR] FortiAuthenticator Unable to Authenticate User Credentials...\nUnexpected Error: {e}\n')
        return 404

'''rollback code
# # Create a new API User Object & Save to Db
# def create_apiuser(request, response):
#         # Create API User Object
#         api_user = APIUser(
#             user = request.user, 
#             issued_time = time.time(),
#             access_token = response.json()['access_token'], 
#             expires_in = response.json()['expires_in'],
#             token_type = response.json()['token_type'],
#             scope = response.json()['scope'],
#             refresh_token = response.json()['refresh_token'],
#             message = response.json()['message'],
#             status = response.json()['status'])
        
#         # Check for Already existing API User against current user(desired: no api user object present!)
#         objects_to_remove = APIUser.objects.filter(user=request.user) # NOTE Test Purposes
#         objects_to_remove.delete()

#         # Save API Object to Database
#         api_user.save()
#         print('[SUCCESS] Created API User!')
'''
def create_apiuser(request, response):
    """
    Create a new APIUser object and save it to the database.

    This function takes a Django HTTP request object and a response object
    from an authentication API call. It creates a new APIUser object with
    relevant attributes and saves it to the database. If an APIUser object
    already exists for the current user, it is deleted before creating the new one.

    :param request: Django HTTP request object.
    :param response: Response object from an authentication API call.

    Example Usage:
    ```
    request = get_authenticated_request()  # Replace with actual authentication logic
    response = auth_credentials()
    if response and response.status_code == 200:
        create_apiuser(request, response)
    else:
        print("Error creating API User.")
    ```
    """

    # Extract relevant information from the authentication response
    auth_data = response.json()

    # Create API User Object
    api_user = APIUser(
        user=request.user,
        issued_time=time.time(),
        access_token=auth_data['access_token'],
        expires_in=auth_data['expires_in'],
        token_type=auth_data['token_type'],
        scope=auth_data['scope'],
        refresh_token=auth_data['refresh_token'],
        message=auth_data['message'],
        status=auth_data['status']
    )

    # Remove existing APIUser objects for the current user (for testing purposes)
    objects_to_remove = APIUser.objects.filter(user=request.user)
    objects_to_remove.delete()

    # Save API User Object to Database
    api_user.save()
    print('[SUCCESS] Created API User!')

'''rollback code
# # CHECK STATUS OF BEARER TOKEN
# def status_token(request):
#     # Check for API User
#     api_user = get_apiuser(request)

#     if api_user != 404:
#         # Check API User Bearer Token Expiry
#         expired = has_expired(api_user)
#         # IF Token Expired attempt Refresh
#         if expired:
#             response = refresh_token(api_user)
#             if response != 404:
#                 print('[UPDATING] API User Bearer Token...')
#                 # Update API User
#                 api_user = APIUser.objects.filter(user=request.user)[0]
#                 api_user.issued_time = time.time()      
#                 api_user.access_token = response.json()['access_token']
#                 api_user.refresh_token = response.json()['refresh_token']
#                 api_user.save()
#                 print('[SUCCESS] API User Updated!')
#                 return True              
#             else:
#                 print('[FATAL] Response was 404!')
#                 return False
#         else:
#             print('Token is VALID(not expired)!')
#             return True     
#     else:
#         response = auth_credentials(request)
#         if response != 404 and response.status_code:
#             create_apiuser(request, response)
#             print('\n\nAPI User Authorized & Created, Successfully Saved to Database!')
#             return True
#         else:
#             return False
'''
def status_token(request):
    """
    Check and update the status of the API User's Bearer Token.

    This function checks the status of the API User's Bearer Token,
    including whether it has expired. If the token has expired, it attempts
    to refresh it. If the refresh is successful, the API User's Bearer Token
    is updated in the database. If there is no existing API User, it attempts
    to authenticate and create a new API User.

    :param request: Django HTTP request object.

    :return: True if the Bearer Token is valid or successfully refreshed,
             False otherwise.

    Example Usage:
    ```
    request = get_authenticated_request()  # Replace with actual authentication logic
    if status_token(request):
        print("Bearer Token is valid or successfully refreshed.")
    else:
        print("Error checking or updating Bearer Token.")
    ```
    """

    # Check for existing API User
    api_user = get_apiuser(request)

    if api_user:
        # Check API User Bearer Token Expiry
        expired = has_expired(api_user)

        # If Token Expired, attempt Refresh
        if expired:
            response = refresh_token(api_user)

            if response and response.status_code == 200:
                print('[UPDATING] API User Bearer Token...')
                # Update API User
                api_user = APIUser.objects.filter(user=request.user).first()
                api_user.issued_time = time.time()
                api_user.access_token = response.json()['access_token']
                api_user.refresh_token = response.json()['refresh_token']
                api_user.save()
                print('[SUCCESS] API User Updated!')
                return True
            else:
                print('[FATAL] Unable to refresh Bearer Token!')
                return False
        else:
            print('Token is VALID (not expired)!')
            return True
    else:
        # No existing API User, attempt to authenticate and create
        response = auth_credentials()

        if response and response.status_code == 200:
            create_apiuser(request, response)
            print('\n\nAPI User Authorized & Created, Successfully Saved to Database!')
            return True
        else:
            return False

'''rollback code
# def api_call(request, sn, fos_api, payload):
#     """Make an API call to the FortiCloud API.

#     This function performs either a GET or POST request to the FortiCloud API
#     based on the provided HTTP request method. It utilizes a session with
#     connection pooling and persists a Bearer Token for authentication.

#     :param request: The HTTP request object, typically from a Django web framework view.
#     :param sn: The serial number of the FortiGate device.
#     :param fos_api: The specific FortiCloud API endpoint.
#     :param payload: The payload to be included in the request for POST method.

#     :return: The response object if the API call is successful (status code 200),
#              otherwise None.

#     :raises: Exception if an unexpected error occurs during the API call.
#     """
#     # Session Persists & Connection Pooling
#     session = requests.Session() 
#     # Session Verification & Tracking
#     session.verify = True # Verification
#     session.trust_env = False # Tracking
    
#     # Define Region Base
#     base_url = 'https://api.fortigate.forticloud.com/forticloudapi/v1/fgt'
#     # Define Full Base
#     api_url = f'{base_url}/{sn}/{fos_api}'

#     response = None
#     api_user = APIUser.objects.get(user=request.user) 

#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {api_user.access_token}'
#     }

#     # Make API Request(GET)
#     if request.method == 'GET':
#         try:
#             print(api_url)
#             response = session.request('get', api_url, headers=headers, verify=False)
#             # print(response.text) # NOTE TESTING PURPOSES
#         except Exception as e:
#             print(f'Unexpected Error: {e}')
#     elif request.method == 'POST':
#         try:
#             response = session.request('post', api_url, headers=headers, json=payload, verify=False)
#             # print(response.text) # NOTE TESTING PURPOSES
#         except Exception as e:
#             print(f'Unexpected Error: {e}')
    
#     if response.status_code == 200:
#         print('[SUCCESS] API Called!', response.status_code)
#         return response
#     else:
#         print('[ERROR] Unable to Call API', response.status_code, response.text)
#         return 505
'''
def api_call(request, sn, fos_api, payload):
    """
    Make an authenticated API call to the FortiCloud API.

    This function performs either a GET or POST request to the FortiCloud API
    based on the provided HTTP request method. It utilizes a session with
    connection pooling and persists a Bearer Token for authentication.

    :param request: Django HTTP request object.
    :param sn: Serial number of the FortiGate device.
    :param fos_api: Specific FortiCloud API endpoint.
    :param payload: Payload for the POST request.

    :return: Response object if the API call is successful (status code 200),
             otherwise None.

    :raises: Exception if an unexpected error occurs during the API call.

    Example Usage:
    ```
    request = get_authenticated_request()  # Replace with actual authentication logic
    serial_number = "FG12345678"
    api_endpoint = "status"
    payload = {"key": "value"}  # For POST requests
    response = api_call(request, serial_number, api_endpoint, payload)
    if response:
        print(f"API Response: {response.json()}")
    else:
        print("API call unsuccessful.")
    ```
    """

    # Session Setup
    session = requests.Session() 
    session.verify = True  # SSL verification enabled
    session.trust_env = False  # Do not read proxy settings from environment

    # API URL Construction
    base_url = 'https://api.fortigate.forticloud.com/forticloudapi/v1/fgt'
    api_url = f'{base_url}/{sn}/{fos_api}'

    # Bearer Token Retrieval
    api_user = APIUser.objects.get(user=request.user) 
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_user.access_token}'
    }

    # Make API Request (GET or POST)
    try:
        method = 'get' if request.method == 'GET' else 'post'
        response = session.request(str(method), api_url, headers=headers, json=payload, verify=False)
        # Uncomment the following line for testing purposes
        # print(response.text)
    except Exception as e:
        print(f'Unexpected Error: {e}')

    # Response Handling
    if response and response.status_code == 200:
        print('[SUCCESS] API Called!', response.status_code)
        return response
    else:
        print('[ERROR] Unable to Call API', response.status_code)
        return None

'''rollback code
# def get_ipsec(request):
#     # FortiOS API Path
#     foc_api = 'api/v2/monitor/vpn/ipsec'    
#     sns = []
#     # Read Serial Numbers from Text File
#     with open('static/res/device_serial_numbers.txt', 'r') as read_sn:
#         sn_rows = read_sn.readlines()
#         for sn_row in sn_rows:
#             sn = sn_row.split('#')[0]
#             sns.append(sn)

#     ipsec_objs = []
#     view_data = {}

#     for sn in sns:
#         # Make API Call
#         response = api_call(request, sn, foc_api, None)
#         if response != None:
#             # Extract Result Data
#             results = response.json()['results']

#             # Iterate Result Data & Normalize
#             for result in results:
#                 tunnel_proxy = result['proxyid']                

#                 # Normalizing - Result Data
#                 core_in = round(result['incoming_bytes'] / (1024.0 * 1024.0))
#                 core_out = round(result['outgoing_bytes'] / (1024.0 * 1024.0))
#                 core_ip = result['tun_id']
#                 core_name = result['name']
#                 core_comm = result['comments']

#             # Normalizing - Proxy Data
#             if tunnel_proxy and len(tunnel_proxy) > 0:
                
#                 proxy_sources = tunnel_proxy[0]['proxy_src'] 

#                 source_subnets = {}                   
#                 for source in proxy_sources:
#                     src_subnet = source['subnet']
#                     source_subnets.update({src_subnet: 'non'})

#                 proxy_destinations = tunnel_proxy[0]['proxy_dst']
                
#                 destination_subnets = {}
#                 for destination in proxy_destinations:
#                     dst_subnet = destination['subnet']
#                     destination_subnets.update({dst_subnet: 'non'})                        

#                 proxy_in = round(tunnel_proxy[0]['incoming_bytes'] / (1024.0 * 1024.0))
#                 proxy_out = round(tunnel_proxy[0]['outgoing_bytes'] / (1024.0 * 1024.0))
#                 proxy_status = tunnel_proxy[0]['status']
#                 proxy_parent = tunnel_proxy[0]['p2name']
                    
#                 src_subnets = []
#                 for key in source_subnets.keys():
#                     src_subnets.append(key)

#                 if len(src_subnets) == 1:
#                     src1 = src_subnets[0]
#                     src2 = 'Non'
#                     src3 = 'Non'
#                     src4 = 'Non'
#                 elif len(src_subnets) == 2:
#                     src1 = src_subnets[0]
#                     src2 = src_subnets[1]
#                     src3 = 'Non'
#                     src4 = 'Non'
#                 elif len(src_subnets) == 3:
#                     src1 = src_subnets[0]
#                     src2 = src_subnets[1]
#                     src3 = src_subnets[2]
#                     src4 = '0.0.0.0'
#                 elif len(src_subnet) >= 4:
#                     src1 = src_subnets[0]
#                     src2 = src_subnets[1]
#                     src3 = src_subnets[2]
#                     src4 = src_subnets[3]
#                 else:
#                     src1 = 'Non'
#                     src2 = 'Non'
#                     src3 = 'Non'
#                     src4 = 'Non'              
                
#                 dst_subnets = []
#                 for key in destination_subnets.keys():
#                     dst_subnets.append(key)

#                 if len(dst_subnets) == 1:
#                     dst1 = dst_subnets[0]
#                     dst2 = 'Non'
#                 elif len(dst_subnets) == 2:
#                     dst1 = dst_subnets[0]
#                     dst2 = dst_subnets[1]
#                 elif len(dst_subnets) == 3:
#                     dst1 = dst_subnets[0]
#                     dst2 = dst_subnets[1]
#                 elif len(dst_subnet) >= 4:
#                     dst1 = dst_subnets[0]
#                     dst2 = dst_subnets[1]
#                 else:
#                     dst1 = 'Non'
#                     dst2 = 'Non'
#             else:
#                 proxy_in = 0.0
#                 proxy_out = 0.0
#                 proxy_status = 'No Proxy Configured!'
#                 proxy_parent = 'No Proxy Configured!'
                
#                 src1 = 'Non'
#                 src2 = 'Non'
#                 src3 = 'Non'
#                 src4 = 'Non'

#                 dst1 = 'Non'
#                 dst2 = 'Non'
                
#             # Define a IPsec/VPN object
#             ipsec_obj = vmc.IPsecVPN(
#                 ip=core_ip,
#                 name=str(core_name).upper(),
#                 comments=str(core_comm),
#                 status=str(proxy_status).upper(),
#                 incoming_core=core_in,
#                 outgoing_core=core_out,
#                 p2name=proxy_parent,
#                 incoming_tunnel=proxy_in,
#                 outgoing_tunnel=proxy_out,
#                 interface='[Interface] Not Yet',
#                 src1=src1, src2=src2, src3=src3, src4=src4, 
#                 dst1=dst1, dst2=dst2)                
#             # Append IPsec/VPN object
#             ipsec_objs.append(ipsec_obj)           
#         else:
#             print('Tunnel Not Connected!')

#     # Sort IPsecVPN objects
#     sorted_ipsec_objs = sorted(ipsec_objs, key=lambda x: x.outgoing_tunnel, reverse=True)  

#     # Update View Data
#     for ipsec_obj in sorted_ipsec_objs:
#         view_obj = {
#             'ip': ipsec_obj.ip,
#             'name': ipsec_obj.name,
#             'comments':ipsec_obj.comments,
#             'status': ipsec_obj.status,
#             'incoming_core': ipsec_obj.incoming_core,
#             'outgoing_core': ipsec_obj.outgoing_core,
#             'p2name': ipsec_obj.p2name,
#             'incoming_tunnel': ipsec_obj.incoming_tunnel,
#             'outgoing_tunnel': ipsec_obj.outgoing_tunnel,
#             'interface': ipsec_obj.interface,
#             'src1': ipsec_obj.src1,'src2': ipsec_obj.src2, 'src3': ipsec_obj.src3, 'src4': ipsec_obj.src4,
#             'dst1': ipsec_obj.dst1, 'dst2': ipsec_obj.dst2
#         }
#         view_data.update({ipsec_obj.p2name: view_obj}) 
    
#     # Return JSON Data to View
#     return JsonResponse(view_data)
'''
def read_serial_numbers(file_path):
    with open(file_path, 'r') as read_sn:
        return [sn.split('#')[0] for sn in read_sn.readlines()]
def get_ipsec(request):
    # FortiOS API Path
    foc_api = 'api/v2/monitor/vpn/ipsec'
    
    sns = read_serial_numbers('static/res/device_serial_numbers.txt')
    ipsec_objs = []
    view_data = {}

    for sn in sns:
        # Make API Call
        response = api_call(request, sn, foc_api, None)
        if response is not None:
            # Extract Result Data
            results = response.json().get('results', [])

            # Handle Proxy Data
            for result in results:
                tunnel_proxy = result.get('proxyid', [])

                # Normalize Result Data
                core_in = round(result.get('incoming_bytes', 0) / (1024.0 * 1024.0))
                core_out = round(result.get('outgoing_bytes', 0) / (1024.0 * 1024.0))
                core_ip = result.get('tun_id', '')
                core_name = result.get('name', '')
                core_comm = result.get('comments', '')

                # Normalize Proxy Data
                proxy_data = tunnel_proxy[0] if tunnel_proxy else {}
                proxy_in = round(proxy_data.get('incoming_bytes', 0) / (1024.0 * 1024.0))
                proxy_out = round(proxy_data.get('outgoing_bytes', 0) / (1024.0 * 1024.0))
                proxy_status = proxy_data.get('status', 'No Proxy Configured!')
                proxy_parent = proxy_data.get('p2name', 'No Proxy Configured!')

                # Normalize Subnets
                source_subnets = [source['subnet'] for source in proxy_data.get('proxy_src', [])]
                destination_subnets = [destination['subnet'] for destination in proxy_data.get('proxy_dst', [])]

                # Sort Subnets
                source_subnets.sort()
                destination_subnets.sort()

                # Create IPsec/VPN object
                ipsec_obj = vmc.IPsecVPN(
                    ip=core_ip,
                    name=str(core_name).upper(),
                    comments=str(core_comm),
                    status=str(proxy_status).upper(),
                    incoming_core=core_in,
                    outgoing_core=core_out,
                    p2name=proxy_parent,
                    incoming_tunnel=proxy_in,
                    outgoing_tunnel=proxy_out,
                    interface='[Interface] Not Yet',
                    src1=source_subnets[0] if source_subnets else '--',
                    src2=source_subnets[1] if len(source_subnets) > 1 else '--',
                    src3=source_subnets[2] if len(source_subnets) > 2 else '--',
                    src4=source_subnets[3] if len(source_subnets) > 3 else '--',
                    dst1=destination_subnets[0] if destination_subnets else '--',
                    dst2=destination_subnets[1] if len(destination_subnets) > 1 else '--'
                )
                # Append IPsec/VPN object
                ipsec_objs.append(ipsec_obj)
        else:
            print(f'Tunnel Not Connected for SN: {sn}')

    # Sort IPsecVPN objects
    sorted_ipsec_objs = sorted(ipsec_objs, key=lambda x: x.outgoing_tunnel, reverse=True)

    # Update View Data
    for ipsec_obj in sorted_ipsec_objs:
        view_obj = {
            'ip': ipsec_obj.ip,
            'name': ipsec_obj.name,
            'comments': ipsec_obj.comments,
            'status': ipsec_obj.status,
            'incoming_core': ipsec_obj.incoming_core,
            'outgoing_core': ipsec_obj.outgoing_core,
            'p2name': ipsec_obj.p2name,
            'incoming_tunnel': ipsec_obj.incoming_tunnel,
            'outgoing_tunnel': ipsec_obj.outgoing_tunnel,
            'interface': ipsec_obj.interface,
            'src1': ipsec_obj.src1, 'src2': ipsec_obj.src2, 'src3': ipsec_obj.src3, 'src4': ipsec_obj.src4,
            'dst1': ipsec_obj.dst1, 'dst2': ipsec_obj.dst2
        }
        view_data[ipsec_obj.p2name] = view_obj

    # Return JSON Data to View
    return JsonResponse(view_data)