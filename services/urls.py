from django.urls import path
from . import fortiauthenticator_api_services,  service_api, views

# Define App Name
app_name = 'services'

urlpatterns = [
    path('token-status/', fortiauthenticator_api_services.status_token, name='status_token'),
    path('get-sites/', views.site_view, name='riybtowl'),
    path('put-interface/', service_api.put_interface, name='kstzzjyf'),
    path('site-interface-revision/', fortiauthenticator_api_services.revert_interface, name='revert_interface'),
]

# NOTE Please use Django REST API before Alpha release!