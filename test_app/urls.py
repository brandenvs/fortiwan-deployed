# Define Imports
from django.urls import path
from . import views

# Define App Name
app_name = 'test_app'

# Define URL patterns - (app)'monitoring'
urlpatterns = [
    path('', views.index, name='index')
]