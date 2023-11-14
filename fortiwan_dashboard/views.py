import requests, json
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from fortiwan_monitor.views import get_tunnels

def index(request):
    return render(request, 'fortiwan_dashboard.html')