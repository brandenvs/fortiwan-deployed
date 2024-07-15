from requests import Response, Session
from .models import APIUser
from django.shortcuts import render
from concurrent.futures import ThreadPoolExecutor as tpe
from concurrent.futures import wait
from .models import Site, UnavailableSite

def get_session(request):
    session = Session()
    api_user = APIUser.objects.get(user=request.user)
    session.headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_user.access_token}', 'Accept-Encoding': 'gzip'}
    return session

def get_site(serial_number, session, base_url):
    api_url = f'{base_url}{serial_number}/api/v2/monitor/vpn/ipsec?format=ip|name|comments|status|proxyid'
    response = session.get(api_url)
    return response

def get_interface(site_name, serial_number, session, base_url):
    api_url = f'{base_url}{serial_number}/api/v2/cmdb/vpn.ipsec/phase1-interface/{site_name}?format=interface&filter=interface=@wan'
    response = session.get(api_url)
    return response

def build_sites(site_data):
    site_objs = []

    for data in site_data:        
        if data.status_code == 200:
            results = data.json().get('results', [])       
            serial_number = data.json().get('serial', '')
        else:     
            results = None

        if results:
            for result_data in results:
                # Site result_data
                core_in = round(result_data.get('incoming_bytes', 0) / (1024.0 * 1024.0))
                core_out = round(result_data.get('outgoing_bytes', 0) / (1024.0 * 1024.0))
                core_ip = result_data.get('tun_id', '')
                core_name = result_data.get('name', '')
                core_comm = result_data.get('comments', '')

                # Tunnel result_data
                tunnel_data = result_data.get('proxyid', [])
                subnet_data = tunnel_data[0] if tunnel_data else {}

                # Subnet data
                proxy_in = round(subnet_data.get('incoming_bytes', 0) / (1024.0 * 1024.0))
                proxy_out = round(subnet_data.get('outgoing_bytes', 0) / (1024.0 * 1024.0))
                proxy_status = subnet_data.get('status', 'No Proxy Configured!')
                proxy_parent = subnet_data.get('p2name', 'No Proxy Configured!')

                source_subnets = [source['subnet'] for source in subnet_data.get('proxy_src', [])]
                destination_subnets = [destination['subnet'] for destination in subnet_data.get('proxy_dst', [])]

                source_subnets.sort()
                destination_subnets.sort()

            # Create IPsec/VPN object
            site_obj = Site(
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
                    src1=source_subnets[0] if source_subnets else '',
                    src2=source_subnets[1] if len(source_subnets) > 1 else '',
                    src3=source_subnets[2] if len(source_subnets) > 2 else '',
                    src4=source_subnets[3] if len(source_subnets) > 3 else '',
                    dst1=destination_subnets[0] if destination_subnets else '',
                    dst2=destination_subnets[1] if len(destination_subnets) > 1 else '',
                    serial_number=serial_number)
            site_objs.append(site_obj)
    return site_objs

def get_interfaces(request, site_objs):
    api_user = APIUser.objects.get(user=request.user)
    session = get_session(request)
    session.headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_user.access_token}', 'Accept-Encoding': 'gzip'}

    base_url = 'https://euapi.fortigate.forticloud.com/forticloudapi/v1/fgt/'

    with tpe() as executor:
        future_interfaces = [executor.submit(
            get_interface, 
            site_obj.name,
            site_obj.serial_number,
            session, 
            base_url) for site_obj in site_objs]
            
        print('Waiting for Site Interface Futures...')
        wait(future_interfaces)    

        # for future in future_interfaces:
        #     print(future.result().json())

        result_interfaces = [future.result() for future in future_interfaces]

        for result_interface  in result_interfaces:        
            _interface = result_interface.json().get('results', [])
            interface_serial = result_interface.json().get('serial', '')
            for site_obj in site_objs:
                if _interface and interface_serial == site_obj.serial_number:
                        site_obj.update_interface(_interface[0].get('interface'))
    return site_objs            

def get_unavailable_sites(request, serial_data):
    session = get_session(request)

    base_url = 'https://euapi.fortigate.forticloud.com/forticloudapi/v1/fgt/'

    with tpe() as executor:
        # Pass additional arguments to the function using functools.partial
        future_sites = [executor.submit(
            get_site, 
            serial_number[0], 
            session, 
            base_url) for serial_number in serial_data]

        print('Waiting for Site Futures...')
        wait(future_sites)

        result_sites = [future.result() for future in future_sites]
    
    # Get site tags    
    
    # Unavailable Sites
    
    site_objs =[]
    
    for site in result_sites:                
        status_code = site.status_code
        # Determine unsuccessful request   
        if status_code != 200:
            
            
            # Locate Serial Number relative to Site's index
            loc = result_sites.index(site)

            print(serial_data[loc][1])
            site_objs.append(UnavailableSite(
                serial_number=serial_data[loc][0],
                serial_tag=serial_data[loc][1],
                site_status=status_code,
                description='Currently Unavailable!'))
        else:
            continue        
    return site_objs                

def get_sites(request, serial_numbers):
    session = get_session(request)

    base_url = 'https://euapi.fortigate.forticloud.com/forticloudapi/v1/fgt/'
    # base_url = 'https://bcfafgmjhb253.bcfa.co.za/v1/fgt/'

    with tpe() as executor:
        # Pass additional arguments to the function using functools.partial
        future_sites = [executor.submit(
            get_site, 
            serial_number, 
            session, 
            base_url) for serial_number in serial_numbers]

        print('Waiting for Site Futures...')
        
        # Wait for the futures in the given sequence to complete.
        wait(future_sites)

        result_sites = [future.result() for future in future_sites]

    site_objs = build_sites(result_sites)

    objs = get_interfaces(request, site_objs)            
    return objs

def put_interface(request):
    if request.method == 'POST':
        site_name = request.POST.get('tunnel_name')
        site_abbr = request.POST.get('tunnel_abbr')
        serial_number = request.POST.get('serial_number')
        current_interface = request.POST.get('tunnel_interface')
    
    change_interface = None
    if current_interface == 'wan1':
        change_interface = 'wan2'
    else:
        change_interface = 'wan1'
    
    payload = {
        'interface': change_interface
    }

    session = get_session(request)

    response = session.request('put', f'https://euapi.fortigate.forticloud.com/forticloudapi/v1/fgt/{serial_number}/api/v2/cmdb/vpn.ipsec/phase1-interface/{site_abbr}', json=payload)
    response_json = response.json()
    print(response_json)
    tunnel_data = {
        'status': response_json.get('status'),
        'http_status': str(response_json.get('http_status')).upper(),
        'revision_changed': response_json.get('revision_changed'),
        'serial': serial_number,
        'interface_before': current_interface,
        'interface_after': change_interface,
        'tunnel_name': site_name,
        'tunnel_abbr': site_abbr
    }
    return render(request, 'ipsec_interface.html', {'tunnel_data': tunnel_data})