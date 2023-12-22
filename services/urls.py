from django.urls import path
from . import fortiauthenticator_api_services,  service_api

# Define App Name
app_name = 'services'

urlpatterns = [
    path('token-status/', fortiauthenticator_api_services.status_token, name='status_token'),
    path('get-site/', service_api.get_sites, name='get_ipsec'),
    path('site-interface-switch/', fortiauthenticator_api_services.post_interface_switch, name='switch_interface'),
    path('site-interface-revision/', fortiauthenticator_api_services.revert_interface, name='revert_interface'),
]

# NOTE Please use Django REST API before Alpha release!