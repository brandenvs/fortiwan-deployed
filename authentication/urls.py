from django.urls import path
from . import views

# Define App Name
app_name = 'authentication'

urlpatterns = [
    # User login
    path('', views.user_login, name='login'), # View
    path('authenticate_user/', views.authenticate_user, name='authenticate_user'), # Logic
    # Create new user
    path('create_user/', views.create_user, name='create_user'), # View
    path('create_new_user/', views.create_new_user, name='create_new_user'), # Logic
    # User profile
    path('show_user/', views.show_user, name='show_user'),    
    # Logout user
    path('logout/', views.logout_user, name='logout'),
    path('remove/', views.remove_user, name='remove')
]