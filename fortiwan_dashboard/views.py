import subprocess, requests, json
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Tunnel
from django.utils import timezone

def index(request):    
    return render(request, 'fortiwan_dashboard.html')    


