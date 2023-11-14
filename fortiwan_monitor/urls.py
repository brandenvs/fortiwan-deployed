# Define Imports
from django.urls import path
from . import views

# Define App Name
app_name = 'fortiwan_monitor'

# Define URL patterns - (app)'monitoring'
urlpatterns = [
    path('', views.index, name='home'),
    path('get_tunnels/', views.get_tunnels, name='get_tunnels'),
]