import requests, time
from django.conf import settings
from authentication.models import APIUser
from . import models as vmc
from django.core.serializers import serialize
from django.http import JsonResponse

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
    session = requests.Session() # Provides Connection Pooling Persistence
    session.verify = False # Disable Verification
    session.trust_env = False # Prevent Tracking

    try:
        # Make a (Refresher) FortiAuthenticator Request
        response = session.request('post', auth_url, headers=headers, json=payload, verify=False) # NOTE VERIFY SHOULD BE TRUE
        if response.status_code == 200:
            print('[SUCCESS] FortiAuthenticator Issued a API User Refreshed Bearer Token!-- ', f'RESPONSE STATUS CODE: {response.status_code}\n')
            return response
        else:
            print('[ERROR] FortiAuthenticator was Unable to Refresh API User Bearer Token-- ', f'RESPONSE STATUS CODE: {response.status_code}\n')
            return response
    except Exception as e:
        print(f'[ERROR] FortiAuthenticator was Unable to Refresh API User Bearer Token...\n{e}\n')
        return 404

# Create a NEW API User object
def auth_credentials():
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
    session = requests.Session() # Provides Connection Pooling Persistence
    session.verify = False # Disable Verification
    session.trust_env = False # Prevent Tracking

     # Calls FortiAuthenticator API POST Request        
    try:
        response = session.request('post', auth_url, headers=headers, json=payload, verify=False)
        if response.status_code == 200:
            print('[SUCCESS] FortiAuthenticator Authorized Bearer & Refresher Tokens-- ', response.status_code, end='\n')
            return response
        else:
            print('[ERROR] FortiAuthenticator was Unable to Authorize Bearer & Refresher Tokens-- ', {response.status_code}, end='\n')
            return response.status_code
    except Exception as e:
        print(f'[ERROR] FortiAuthenticator Unable to Authenticate User Credentials...\nUnexpected Error: {e}\n')
        return 404

# Create a new API User Object & Save to Db
def create_apiuser(request, response):
        # Create API User Object
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
        
        # Check for Already existing API User against current user(desired: no api user object present!)
        objects_to_remove = APIUser.objects.filter(user=request.user) # NOTE Test Purposes
        objects_to_remove.delete()

        # Save API Object to Database
        api_user.save()
        print('[SUCCESS] Created API User!')

# CHECK STATUS OF BEARER TOKEN
def status_token(request):
    # Check for API User
    api_user = get_apiuser(request)

    if api_user != 404:
        # Check API User Bearer Token Expiry
        expired = has_expired(api_user)
        # IF Token Expired attempt Refresh
        if expired:
            response = refresh_token(api_user)
            if response != 404:
                print('[UPDATING] API User Bearer Token...')
                # Update API User
                api_user = APIUser.objects.filter(user=request.user)[0]
                api_user.issued_time = time.time()      
                api_user.access_token = response.json()['access_token']
                api_user.refresh_token = response.json()['refresh_token']
                api_user.save()
                print('[SUCCESS] API User Updated!')
                return True              
            else:
                print('[FATAL] Response was 404!')
                return False
        else:
            print('Token is VALID(not expired)!')
            return True     
    else:
        response = auth_credentials(request)
        if response != 404 and response.status_code:
            create_apiuser(request, response)
            print('\n\nAPI User Authorized & Created, Successfully Saved to Database!')
            return True
        else:
            return False

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
            # print(response.text) # NOTE TESTING PURPOSES
        except Exception as e:
            print(f'Unexpected Error: {e}')
    elif request.method == 'POST':
        try:
            response = session.request('post', api_url, headers=headers, json=payload, verify=False)
            # print(response.text) # NOTE TESTING PURPOSES
        except Exception as e:
            print(f'Unexpected Error: {e}')
    
    if response.status_code == 200:
        print('[SUCCESS] API Called!', response.status_code)
        return response
    else:
        print('[ERROR] Unable to Call API', response.status_code, response.text)
        return 505

def get_ipsec(request):
    # FortiOS API Path
    foc_api = 'api/v2/monitor/vpn/ipsec'    
    sns = []
    # Read Serial Numbers from Text File
    with open('static/res/device_serial_numbers.txt', 'r') as read_sn:
        sn_rows = read_sn.readlines()
        for sn_row in sn_rows:
            sn = sn_row.split('#')[0]
            sns.append(sn)

    ipsec_objs = []
    view_data = {}

    for sn in sns:
        # Make API Call
        response = api_call(request, sn, foc_api, None)
        if response != 505:
            # Extract Result Data
            results = response.json()['results']

            # Iterate Result Data & Normalize
            for result in results:
                tunnel_proxy = result['proxyid']                

                # Normalizing - Result Data
                core_in = round(result['incoming_bytes'] / (1024.0 * 1024.0))
                core_out = round(result['outgoing_bytes'] / (1024.0 * 1024.0))
                core_ip = result['tun_id']
                core_name = result['name']
                core_comm = result['comments']

            # Normalizing - Proxy Data
            if tunnel_proxy and len(tunnel_proxy) > 0:
                
                proxy_sources = tunnel_proxy[0]['proxy_src'] 

                source_subnets = {}                   
                for source in proxy_sources:
                    src_subnet = source['subnet']
                    source_subnets.update({src_subnet: 'non'})

                proxy_destinations = tunnel_proxy[0]['proxy_dst']
                
                destination_subnets = {}
                for destination in proxy_destinations:
                    dst_subnet = destination['subnet']
                    destination_subnets.update({dst_subnet: 'non'})                        

                proxy_in = round(tunnel_proxy[0]['incoming_bytes'] / (1024.0 * 1024.0))
                proxy_out = round(tunnel_proxy[0]['outgoing_bytes'] / (1024.0 * 1024.0))
                proxy_status = tunnel_proxy[0]['status']
                proxy_parent = tunnel_proxy[0]['p2name']
                    
                src_subnets = []
                for key in source_subnets.keys():
                    src_subnets.append(key)

                if len(src_subnets) == 1:
                    src1 = src_subnets[0]
                    src2 = 'Non'
                    src3 = 'Non'
                    src4 = 'Non'
                elif len(src_subnets) == 2:
                    src1 = src_subnets[0]
                    src2 = src_subnets[1]
                    src3 = 'Non'
                    src4 = 'Non'
                elif len(src_subnets) == 3:
                    src1 = src_subnets[0]
                    src2 = src_subnets[1]
                    src3 = src_subnets[2]
                    src4 = '0.0.0.0'
                elif len(src_subnet) >= 4:
                    src1 = src_subnets[0]
                    src2 = src_subnets[1]
                    src3 = src_subnets[2]
                    src4 = src_subnets[3]
                else:
                    src1 = 'Non'
                    src2 = 'Non'
                    src3 = 'Non'
                    src4 = 'Non'              
                
                dst_subnets = []
                for key in destination_subnets.keys():
                    dst_subnets.append(key)

                if len(dst_subnets) == 1:
                    dst1 = dst_subnets[0]
                    dst2 = 'Non'
                elif len(dst_subnets) == 2:
                    dst1 = dst_subnets[0]
                    dst2 = dst_subnets[1]
                elif len(dst_subnets) == 3:
                    dst1 = dst_subnets[0]
                    dst2 = dst_subnets[1]
                elif len(dst_subnet) >= 4:
                    dst1 = dst_subnets[0]
                    dst2 = dst_subnets[1]
                else:
                    dst1 = 'Non'
                    dst2 = 'Non'
            else:
                proxy_in = 0.0
                proxy_out = 0.0
                proxy_status = 'No Proxy Configured!'
                proxy_parent = 'No Proxy Configured!'
                
                src1 = 'Non'
                src2 = 'Non'
                src3 = 'Non'
                src4 = 'Non'

                dst1 = 'Non'
                dst2 = 'Non'
                
            # Define a IPsec/VPN object
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
                src1=src1, src2=src2, src3=src3, src4=src4, 
                dst1=dst1, dst2=dst2)                
            # Append IPsec/VPN object
            ipsec_objs.append(ipsec_obj)           
        else:
            print('Tunnel Not Connected!')

    # Sort IPsecVPN objects
    sorted_ipsec_objs = sorted(ipsec_objs, key=lambda x: x.outgoing_tunnel, reverse=True)  

    # Update View Data
    for ipsec_obj in sorted_ipsec_objs:
        view_obj = {
            'ip': ipsec_obj.ip,
            'name': ipsec_obj.name,
            'comments':ipsec_obj.comments,
            'status': ipsec_obj.status,
            'incoming_core': ipsec_obj.incoming_core,
            'outgoing_core': ipsec_obj.outgoing_core,
            'p2name': ipsec_obj.p2name,
            'incoming_tunnel': ipsec_obj.incoming_tunnel,
            'outgoing_tunnel': ipsec_obj.outgoing_tunnel,
            'interface': ipsec_obj.interface,
            'src1': ipsec_obj.src1,'src2': ipsec_obj.src2, 'src3': ipsec_obj.src3, 'src4': ipsec_obj.src4,
            'dst1': ipsec_obj.dst1, 'dst2': ipsec_obj.dst2
        }
        view_data.update({ipsec_obj.p2name: view_obj}) 
    
    # Return JSON Data to View
    return JsonResponse(view_data)
