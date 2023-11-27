from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from fortiwan_services.services import get_token
import os
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    # Get Bearer Token
    get_token(request)
    return render(request, 'fortiwan_dashboard.html')

# bearer_token = os.getenv('BEARER_TOKEN')

