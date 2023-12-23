import requests
from django.conf import settings
from .models import APIUser
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from concurrent.futures import ThreadPoolExecutor as tpe
from concurrent.futures import wait
from .models import Site

def get_session():
    session = requests.Session()
    return session

def get_site(serial_number, session, base_url):
    response = session.get(base_url + serial_number + '/api/v2/monitor/vpn/ipsec?format=ip|name|comments|status|proxyid')
    return response

def get_interface(site_name, serial_number, session, base_url):
    api_url = f'{base_url}{serial_number}/api/v2/cmdb/vpn.ipsec/phase1-interface/{site_name}?format=interface&filter=interface=@wan'
    response = session.get(api_url)
    return response

def process_data(response):
    pass

def decouple_data(coupled_data):
    pass

def build_site(site_data):
    site_objs = []

    for data in site_data:
        
        if data.status_code == 200:
            results = data.json().get('results', [])       
            serial_number = data.json().get('serial', '')

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
    session = get_session()
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

def get_sites(request, serial_numbers):
    api_user = APIUser.objects.get(user=request.user)
    session = get_session()
    session.headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_user.access_token}', 'Accept-Encoding': 'gzip'}

    base_url = 'https://euapi.fortigate.forticloud.com/forticloudapi/v1/fgt/'
    with tpe() as executor:
        # Pass additional arguments to the function using functools.partial
        future_sites = [executor.submit(
            get_site, 
            serial_number, 
            session, 
            base_url) for serial_number in serial_numbers]

        print('Waiting for Site Futures...')
        wait(future_sites)

        result_sites = [future.result() for future in future_sites]

    site_objs = build_site(result_sites)

    objs = get_interfaces(request, site_objs)

    return objs



def dynamic_call():
    pass
