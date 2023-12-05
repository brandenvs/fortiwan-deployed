# IMPORTS
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User

# Login User(View) Function - Handles Login Web Page. Passing User Object if User is Logged In.
def user_login(request):
    if request.user.is_authenticated:
        current_user = request.user
        return HttpResponseRedirect(reverse('fortiwan_dashboard:home'))
    else:
        current_user = None
        return render(request, 'authentication/login.html')

# Create User Function - Create a New User to Database
def create_new_user(request):
    if request.user.is_authenticated:
        current_user = request.user
        print("User is trying to create a NEW USER while still logged in...")
        return render(request, 'authentication/create_user.html', {'current_user': current_user})
           
    if request.method == 'POST':
        # Fetch User Details from Web Page
        first_name = request.POST.get('firstname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # Create a New User instance and Set Attributes
            new_user = User.objects.create_user(username=username, password=password)
            # Set Firstname
            new_user.first_name = first_name
            # Set Is? - Staff
            new_user.is_staff = False
            # Set Is? - Superuser
            new_user.is_superuser = False
            # Save User to Database
            new_user.save()
            print("Successfully Added New User to Database")
            print(f"USERNAME - {username}\nPassword(raw) - {password}\nFirstname - {first_name}")
            # Redirect User to Profile
            return HttpResponseRedirect(reverse('authentication:show_user'))   
        # Catch the exception
        except Exception as ex:            
            # Get the Error Message
            error_message = str(ex)
            # Render Create User View and, Pass the Error Message to View
            return render(request, 'authentication/create_user.html', {'error_message': error_message})
    
    # Render Initial Create User View
    return render(request, 'authentication/create_user.html')

# Create User Function(Redirects...)
def user_create(request):
    if request.method == 'POST':
        # Get User Details from Web Page
        first_name = request.POST.get('firstname')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Create a New User & Save to Database
        try:
            user = User.objects.create_user(username=username, password=password)
            user.first_name = first_name
            user.is_staff = False
            user.is_superuser = False
            # Save user to Db
            user.save()
            # Redirect user
            return HttpResponseRedirect(reverse('dashboard:home'))
        except Exception as ex:
            print(f'SOMETHING WENT WRONG!\nError:\n{str(ex)}')
            return render(request, 'authentication/user_create.html', {'error': str(ex)})
    # Redirect User - create_new_user
    return HttpResponseRedirect(reverse('authentication:create_new_user'))

# Create User View
def create_user(request):
    # Render View
    return render(request, 'authentication/create_user.html')

# Login User(Authentication) Function - Handles Login Logic.
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
        return render(request, 'authentication/login.html', {'error_message': error_message})
    else:
        # Login user 
        login(request, user)
        return HttpResponseRedirect(reverse('fortiwan_dashboard:home'))

# Renders View & Model - User Profile
def show_user(request):
    print(request.user.username)
    if request.user.is_authenticated:
        return render(request, 'authentication/user.html', {
            "username": request.user.username,
            "password": request.user.password,
            "firstname": request.user.first_name })
    else:
        return HttpResponseRedirect(reverse('authentication:login'))

# Remove the authenticated user's ID from the request and flush their session data
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('authentication:login'))
# FILE-LOGIC END
# Please Note:  '''All The Code in this File was Contributed by: Branden van Staden''' Thank you!