from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from myfortiwan.services import get_token
import os

def index(request):
    if request.user.is_authenticated:
        get_token(request)
        bearer_token = os.getenv('BEARER_TOKEN')
        print(f'YOUR BEARER TOKEN: {bearer_token}')
        return render(request, 'fortiwan_dashboard.html')
    else:
        return HttpResponseRedirect(reverse('authentication:login'))

