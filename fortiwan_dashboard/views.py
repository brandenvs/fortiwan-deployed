from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from fortiwan_services.fortiauthenticator_api_services import status_token, get_ipsec, read_serial_numbers
import os
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    status_token(request)
    sns = read_serial_numbers('static/res/device_serial_numbers.txt')
    return render(request, 'fortiwan_dashboard.html', {'sns': sns})
