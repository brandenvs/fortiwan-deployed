#################################################
# File: urls.py 
# Maps URL paths, patterns web application: users
#################################################
# Define Imports
from django.urls import path
from . import views

# Define App Name
app_name = 'authentication'

# Define URL patterns - (app)'users'
urlpatterns = [
    # URL Pattern - User Login
    path('', views.user_login, name='login'),
    # URL Pattern - Create New User
    path('create_user/', views.create_user, name='create_user'),
    # URL Pattern - POST Create New User
    path('create_new_user/', views.create_new_user, name='create_new_user'),
    # URL Pattern - Authenticate users
    path('authenticate_user/', views.authenticate_user, name='authenticate_user'),
    # URL Pattern - Show user details
    path('show_user/', views.show_user, name='show_user'),
    # URL Pattern - Logout user
    path('logout/', views.logout_user, name='logout')
]



