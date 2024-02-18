from django.urls import path
from . import fortiauthenticator_api_services,  service_api, views

# Define App Name
app_name = 'services'

urlpatterns = [
    path('token-status/', fortiauthenticator_api_services.status_token, name='status_token'),
    path('get-sites/', views.sites_view, name='riybtowl'),
    path('get-site/', views.site_view, name='hciijyfr'),
    path('get-suspended/', views.sites_suspended, name='suspended'),
    path('put-interface/', service_api.put_interface, name='kstzzjyf'),
]

# NOTE Please use Django REST API before Alpha release!