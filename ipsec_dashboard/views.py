from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from services.views import read_sn
from services.fortiauthenticator_api_services import status_token

@login_required
def index(request):
    status_token(request)
    sn_data = read_sn('static/res/device_serial_numbers.txt')

    sn_site_dict = {}
    for data in sn_data:
        sn_site_dict.update({data[0]: data[1] })
    return render(request, 'ipsec_dashboard.html', {'view_data': sn_site_dict})

def result_view(request, tunnel_data):
    status_token(request)
    return render(request, 'ipsec_interface.html', {'tunnel_data': tunnel_data})

