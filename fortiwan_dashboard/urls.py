# Define Imports
from django.urls import path
from . import views

# Define App Name
app_name = 'fortiwan_dashboard'

# Define URL patterns - (app)'monitoring'
urlpatterns = [
    path('', views.index, name='home'),
    path('fetch_tunnels/', views.fetch_tunnels, name='fetch_tunnels'),
]