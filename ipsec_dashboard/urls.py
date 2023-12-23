from django.urls import path
from . import views

# Define App Name
app_name = 'ipsec_dashboard'

urlpatterns = [
    path('', views.index, name='home'),
]