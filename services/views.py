import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import service_api
from django.http import JsonResponse

def read_serial_numbers(file_path):
    with open(file_path, 'r') as read_sn:
        return [sn.split('#')[0] for sn in read_sn.readlines()]
    
def site_view(request):
    view_data = {}
    
    serial_numbers = read_serial_numbers('static/res/device_serial_numbers.txt')
    
    site_objs  = service_api.get_sites(request, serial_numbers)

    # Sort IPsecVPN objects
    sorted_ipsec_objs = sorted(site_objs, key=lambda x: x.outgoing_tunnel, reverse=True)    

    # Update View Data
    for site_obj in sorted_ipsec_objs:
        view_obj = {
            'ip': site_obj.ip,
            'name': site_obj.name,
            'comments': site_obj.comments,
            'status': site_obj.status,
            'incoming_core': site_obj.incoming_core,
            'outgoing_core': site_obj.outgoing_core,
            'p2name': site_obj.p2name,
            'incoming_tunnel': site_obj.incoming_tunnel,
            'outgoing_tunnel': site_obj.outgoing_tunnel,
            'interface': site_obj.interface,
            'src1': site_obj.src1, 'src2': site_obj.src2, 'src3': site_obj.src3, 'src4': site_obj.src4,
            'dst1': site_obj.dst1, 'dst2': site_obj.dst2,
            'serial_number': site_obj.serial_number
        }
        view_data[site_obj.name] = view_obj    
    return JsonResponse(view_data)
