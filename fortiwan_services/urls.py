# Define Imports
from django.urls import path
from . import fortiauthenticator_api_services, views

# Define App Name
app_name = 'fortiwan_services'

# Define URL patterns - (app)'monitoring'
urlpatterns = [
    path('check-for-token/', fortiauthenticator_api_services.status_token, name='status_token'),
    path('ipsec-vpn-foc-monitor/', fortiauthenticator_api_services.get_ipsec, name='get_ipsec'),
    path('ipsec-vpn-foc-configure/', fortiauthenticator_api_services.post_interface_switch, name='switch_interface'),
    # path('tunnel-overview/', fortiauthenticator_api_services.post_interface_switch, name='tunnel_overview'),

]