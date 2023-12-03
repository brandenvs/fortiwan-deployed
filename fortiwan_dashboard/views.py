from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from fortiwan_services.fortiauthenticator_api_services import status_token, get_ipsec
import os
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    status_token(request)
    return render(request, 'fortiwan_dashboard.html')
