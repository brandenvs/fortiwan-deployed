# Define Imports
from django.urls import path
from . import fortiauthenticator_api_services

# Define App Name
app_name = 'fortiwan_services'

# Define URL patterns - (app)'monitoring'
urlpatterns = [
    path('check-for-token/', fortiauthenticator_api_services.status_token, name='status_token'),
    path('get-tunnels/', fortiauthenticator_api_services.get_tunnels, name='get_tunnels'),

]