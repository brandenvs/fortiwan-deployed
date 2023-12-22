import requests
from django.conf import settings
from .models import APIUser
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import concurrent.futures

def get_session():
    session = requests.Session()
    return session

def get_data(serial_number, session, base_url, headers):
    response = session.get(base_url + serial_number + '/api/v2/monitor/vpn/ipsec?format=ip|name|comments|status|proxyid', headers=headers)
    print(response.status_code, response.json())

def get_sites(request):
    api_user = APIUser.objects.get(user=request.user)
    serial_numbers = ['FGT60FTK2109D2Z2', 'FGT60FTK2109D33E']
    session = get_session()
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_user.access_token}', 'Accept-Encoding': 'gzip'}

    base_url = 'https://euapi.fortigate.forticloud.com/forticloudapi/v1/fgt/'

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Pass additional arguments to the function using functools.partial
        futures = [executor.submit(get_data, serial_number, session, base_url, headers) for serial_number in serial_numbers]

        # Wait for all futures to complete
        concurrent.futures.wait(futures)

        # Retrieve results (if needed)
        results = [future.result() for future in futures]

    # Your code continues here after all requests are done
        print(results)
    # Example: JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'success'})







def dynamic_call():
    pass
