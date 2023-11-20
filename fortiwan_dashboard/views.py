from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from fortiwan_monitor.views import get_tunnels

def index(request):
    if request.user.is_authenticated:
        return render(request, 'fortiwan_dashboard.html')
    else:
        return HttpResponseRedirect(reverse('authentication:login'))

