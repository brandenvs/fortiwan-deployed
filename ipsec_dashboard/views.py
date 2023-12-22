from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from services.fortiauthenticator_api_services import status_token, read_serial_numbers

@login_required
def index(request):
    status_token(request)
    sns = read_serial_numbers('static/res/device_serial_numbers.txt')
    return render(request, 'ipsec_dashboard.html', {'sns': sns})
