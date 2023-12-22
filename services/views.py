import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def tunnel_overview(request, tunnel_data):
    # Retrieve the tunnel_data from the request's GET parameters
    print(tunnel_data)
    # Convert the tunnel_data string to a dictionary using json.loads
    tunnel_data_dict = json.loads(tunnel_data) if tunnel_data else {}
    print(tunnel_data_dict)

    return render(request, 'tunnel_overview.html', {'tunnel_data_dict': tunnel_data_dict})

