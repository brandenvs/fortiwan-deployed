from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from myfortiwan.services import get_token
import os

def index(request):
    # Check User is Logged In
    if request.user.is_authenticated:
        # Get Bearer Token
        get_token(request)

        # bearer_token = os.getenv('BEARER_TOKEN')
        # print(f'YOUR BEARER TOKEN: {bearer_token}') NOTE TEST PURPOSES
        return render(request, 'fortiwan_dashboard.html')
    else:
        # Reverse Login Page(if user is NOT logged in...)
        return HttpResponseRedirect(reverse('authentication:login'))

