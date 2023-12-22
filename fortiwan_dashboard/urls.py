# Define Imports
from django.urls import path
from . import views

# Define App Name
app_name = 'fortiwan_dashboard'

# Define URL patterns - (app)'monitoring'
urlpatterns = [
    path('', views.index, name='home'),
    path('soz/', views.offline, name='offline'),
]