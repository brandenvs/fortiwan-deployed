from django.shortcuts import render

def index(request):
    return render(request, 'fortiwan_config.html')
