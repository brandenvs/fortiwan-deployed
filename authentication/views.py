# IMPORTS
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def user_login(request):
    if request.user.is_authenticated:
        return redirect('ipsec_dashboard:home')
    else:
        return render(request, 'login.html')

def authenticate_user(request):
    username = request.POST['username']
    password = request.POST['password']    
    # Authorize user
    user = authenticate(username=username, password=password)
    # User is NOT Authenticated
    if user is None:
        # Update result parameter to pass to view
        error_message = "Invalid Username or Password!"
        # Construct reverse URL for Http Response Redirect
        return render(request, 'login.html', {'error_message': error_message})
    else:
        # Login user 
        login(request, user)
        return HttpResponseRedirect(reverse('ipsec_dashboard:home'))

@login_required
def create_new_user(request):
    if request.method == 'POST':
        # Fetch User Details from Web Page
        first_name = request.POST.get('firstname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # Create a New User instance and Set Attributes
            new_user = User.objects.create_user(username=username, password=password)
            new_user.first_name = first_name
            new_user.is_staff = False
            new_user.is_superuser = False

            # Save User to Database
            new_user.save()
            # Redirect User to Profile
            return HttpResponseRedirect(reverse('authentication:show_user'))   
        
        # Catch the exception
        except Exception as ex:
            # Render Create User View and, Pass the Error Message to View
            return render(request, 'create_user.html', {'error_message': str(ex)})
    
    # Render Initial Create User View
    return render(request, 'create_user.html')

@login_required
def create_user(request):
    # Render View
    return render(request, 'create_user.html')

@login_required
def show_user(request):
    return render(request, 'user.html', { "username": request.user.username, "password": request.user.password, "firstname": request.user.first_name })

@login_required
def logout_user(request):
    logout(request)
    return redirect('authentication:login')