import requests, time, certifi, urllib3
from requests import Request, Session
from django.conf import settings
from .models import APIUser
from . import models as vmc
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

session = urllib3.PoolManager(
        cert_reqs="CERT_REQUIRED",
        ca_certs=certifi.where())

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
    none_flag = False
    try:
        # Attempt to retrieve APIUser associated with the user in the request
        api_user = APIUser.objects.get(user=request.user)

        # Check if the username is None
        if api_user.user.username is None:
            none_flag = True

    except APIUser.DoesNotExist:
        # APIUser not found
        none_flag = True

    except Exception as e:
        # Other unexpected errors
        none_flag = True

    if none_flag:
        # Log a message and return 404 status if no APIUser is found
        print(f'[Not Found] No API User Found for: {request.user.username}...\n')
        return 404

    # Log success and return the APIUser object
    print('[SUCCESS] Found API User! -- USERNAME:', api_user.user.username, end='\n')
    return api_user

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

    if api_user != 404:
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

def api_call(request, serial_number, fos_area, payload):
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

    # API URL Construction
    base_url = 'https://api.fortigate.forticloud.com/forticloudapi/v1/fgt'
    # api_url = urljoin(base_url, f'{serial_number}/{fos_area}')
    api_url = f'{base_url}/{serial_number}/{fos_area}'

    # Bearer Token Retrieval
    api_user = APIUser.objects.get(user=request.user) 
    session.headers = { 'Content-Type': 'application/json', 'Authorization': f'Bearer {api_user.access_token}','Accept-Encoding': 'gzip' }
    
    # Make API Request (GET or POST)
    try:
        method = 'get' if request.method == 'GET' else 'put' # Sleek
        print(f'\nCALLING({method}): ', api_url, end='\n')
        # response = session.request(str(method), api_url, headers=headers, json=payload)
        if method == 'get':
            resp = session.request(str(method), api_url)  
            # response = session.request(str(method), api_url)
        else:
            resp = session.request(str(method), api_url, json=payload)
        # Uncomment the following line for testing purposes
        # print(response.data.decode())
    except Exception as e:
        print(f'Unexpected Error: {e}')
        return None

    # Response Handling
    if resp and resp.status == 200:
        print('[SUCCESS] API Called!', resp.status)
        return resp
    else:
        print('[ERROR] Unable to Call API', resp.status)
        return None

def read_serial_numbers(file_path):
    with open(file_path, 'r') as read_sn:
        return [sn.split('#')[0] for sn in read_sn.readlines()]

def get_ipsec(request):
    # FortiOS API Path
    foc_api = 'api/v2/monitor/vpn/ipsec?format=ip|name|comments|status|proxyid'

    sns = read_serial_numbers('static/res/device_serial_numbers.txt')
    ipsec_objs = []
    view_data = {}

    # NOTE Bespoke Solution
    firewall_teraco = sns.pop(0)
    print(f'\nremoved serial number: "{firewall_teraco}"\n')

    # Bearer Token Retrieval
        
    for sn in sns:
        # Make API Call
        response = api_call(request, sn, foc_api, None)
            
        if response and response.status == 200:
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
                        interface='non',
                        src1=source_subnets[0] if source_subnets else '--',
                        src2=source_subnets[1] if len(source_subnets) > 1 else '--',
                        src3=source_subnets[2] if len(source_subnets) > 2 else '--',
                        src4=source_subnets[3] if len(source_subnets) > 3 else '--',
                        dst1=destination_subnets[0] if destination_subnets else '--',
                        dst2=destination_subnets[1] if len(destination_subnets) > 1 else '--',
                        serial_number=sn
                    )                
                get_interface(request, ipsec_obj)

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
                'dst1': ipsec_obj.dst1, 'dst2': ipsec_obj.dst2,
                'serial_number': ipsec_obj.serial_number
            }
            view_data[ipsec_obj.name] = view_obj
    
    session.clear()
    # for key,val in session.pools.items():
    #     print(key, val)
    # # Return JSON Data to View
    return JsonResponse(view_data)

def get_interface(request, ipsec_obj):
    fos_api = f'api/v2/cmdb/vpn.ipsec/phase1-interface/{ipsec_obj.name}?format=interface&filter=interface=@wan'

    name_split = ipsec_obj.name
    name_split = str(name_split).split('_')

    if len(name_split) <= 2:
        response_interface = api_call(request, ipsec_obj.serial_number, fos_api, None)
        if response_interface is not None:
            # Extract Result Data
            results = response_interface.json().get('results', [])
            for result in results:
                interface = result.get('interface', '')
                ipsec_obj.update_interface(interface)

def post_interface_switch(request):
    if request.method == 'POST':
        tunnel_name = request.POST.get('tunnel_name')
        tunnel_abbr = request.POST.get('tunnel_abbr')
        serial_number = request.POST.get('serial_number')
        tunnel_interface = request.POST.get('tunnel_interface')

        fos_area = f'api/v2/cmdb/vpn.ipsec/phase1-interface/{tunnel_abbr}'

        print(f'serial_number: {serial_number}\nname: {tunnel_name}\ninterface: {tunnel_interface}')

        if tunnel_interface == 'wan1':
            new_tunnel_interface = 'wan2'
        elif tunnel_interface == 'wan2':
            new_tunnel_interface = 'wan1'
        else:
            new_tunnel_interface = 'No Interface'

        # Define JSON Payload
        payload = {
            'interface': new_tunnel_interface
        }

        response = api_call(request, serial_number, fos_area, payload)
        response_json = response.json()
        print(response_json)

        tunnel_data = {
            'mkey': response_json['mkey'],
            'status': response_json['status'],
            'http_status': str(response_json['http_status']).upper(),
            'revision_changed': response_json['revision_changed'],
            'serial': response_json['serial'],
            'interface_before': tunnel_interface,
            'interface_after': new_tunnel_interface,
            'tunnel_name': tunnel_name,
            'tunnel_abbr': tunnel_abbr
        }
        return render(request, 'tunnel_overview.html', {'tunnel_data': tunnel_data})

def revert_interface(request):
    if request.method == 'POST':
        interface_before = request.POST.get('interface_before')
        tunnel_serial = request.POST.get('tunnel_serial')
        tunnel_abbr = request.POST.get('tunnel_abbr')

        fos_area = f'api/v2/cmdb/vpn.ipsec/phase1-interface/{tunnel_abbr}'

        if interface_before == 'wan1':
            new_tunnel_interface = 'wan2'
        elif interface_before == 'wan2':
            new_tunnel_interface = 'wan1'
        else:
            new_tunnel_interface = 'No Interface'

        # Define JSON Payload
        payload = {
            'interface': new_tunnel_interface
        }

        response = api_call(request, tunnel_serial, fos_area, payload)
        print(response.data.decode())
        return HttpResponse(response.data.decode())
