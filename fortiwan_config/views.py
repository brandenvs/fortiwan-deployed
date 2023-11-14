from django.shortcuts import render
from django.contrib.auth.decorators import login_required

app_name = 'fortiwan_config'

@login_required
def index(request):
    return render(request, 'fortiwan_config.html')
