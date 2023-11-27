import requests, time
from django.conf import settings
from authentication.models import APIUser

# Firewall Model
class Firewall:
    def __init__(self, ip, name, comment, status, incoming_core, outgoing_core, incoming_tunnel, outgoing_tunnel, p2name, interface):
        self.ip = ip
        self.name = name        
        self.comment = comment
        self.status = status
        self.incoming_core = incoming_core
        self.outgoing_core = outgoing_core
        self.p2name = p2name
        self.incoming_tunnel = incoming_tunnel
        self.outgoing_tunnel = outgoing_tunnel
        self.interface = interface 

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
def auth_credentials(request):
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
    sns = ['FGT60FTK2109D2Z2']

    view_dict = {}
    tunnel_responses = []
    firewalls = []
    vpn_tunnels = None

    for sn in sns:
        # API Call Variables
        response = api_call(request, sn, foc_api, None)
        tunnel_responses.append(response.json())      

        for tunnel in tunnel_responses:
            firewall = dict(tunnel['results'])
            firewall_proxy = firewall['proxyid']
            print(firewall.get('tun_id'), firewall_proxy[0]('p2name'))        
         
    try:       

            # if tunnel['results']:
            #     firewall_obj = Firewall(
            #         ip = firewall['tun_id'],
            #         name = firewall['name'],
            #         comment = firewall['comment'],
            #         status = firewall_proxy['status'],
            #         incoming_core = firewall['incoming_bytes'],
            #         outgoing_core = firewall['outgoing_bytes'],
            #         p2name = firewall_proxy['p2name'],
            #         incoming_tunnel = firewall_proxy['incoming_bytes'],
            #         outgoing_tunnel = firewall['outgoing_bytes'],
            #         interface = 'NOT IMPLEMENTED YET!')
            
            print(firewall_obj.name)
            # firewall = tunnel.get('results', [])            
            # proxy = firewall.get('proxyid', [])

            # if len(firewall) > 0: # Check that the object has any vpn stats
            #     interface = 'non'
            #     firewall_obj = Firewall(
            #         ip=firewall.get('tun_id'), 
            #         name=firewall.get('name'), 
            #         comment=firewall.get('comments'), 
            #         status=proxy[0]['status'], 
            #         incoming_core=firewall.get('incoming_bytes'), 
            #         incoming_core=firewall.get('outgoing_bytes'),
            #         p2name=proxy[0]['p2name'],
            #         incoming_tunnel=proxy[0]['incoming_bytes'],
            #         outgoing_tunnel=proxy[0]['outgoing_bytes'],
            #         interface=interface)
            #     firewalls.append(firewall_obj)    
    except Exception as e:
        print('ERROR OCCURRED: ', e)
        return e    
            
    for firewall_obj in firewalls: 
        view_dict.update({firewall_obj.name:{
            'ip': firewall_obj.ip, 
            'name': firewall_obj.name, 
            'comment': firewall_obj.comment, 
            'status': firewall_obj.status, 
            'incoming_core': round(firewall_obj.incoming_core / (1024.0 * 1024.0)), 
            'outgoing_core': round(firewall_obj.outgoing_core / (1024.0 * 1024.0)), 
            'p2name': firewall_obj.p2name, 
            'incoming_tunnel': round(firewall_obj.incoming_tunnel / (1024.0 * 1024.0)),
            'outgoing_tunnel': round(firewall_obj.outgoing_tunnel / (1024.0 * 1024.0)),
            'interface': firewall_obj.interface}})
    return view_dict


   
    