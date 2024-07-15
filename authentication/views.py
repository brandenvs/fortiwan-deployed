# IMPORTS
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse


def user_login(request):
    if request.user.is_authenticated:
        return redirect("ipsec_dashboard:home")
    else:
        return render(request, "login.html")


def authenticate_user(request):
    _username = request.POST["username"]
    password = request.POST["password"]

    username = str(_username).lower()

    # Authorize user
    user = authenticate(username=username, password=password)
    # User is NOT Authenticated
    if user is None:
        # Update result parameter to pass to view
        error_message = "Invalid Username or Password!"
        # Construct reverse URL for Http Response Redirect
        return render(request, "login.html", {"error_message": error_message})
    else:
        # Login user
        login(request, user)
        return HttpResponseRedirect(reverse("ipsec_dashboard:home"))


# Define a test function to check if the user has is_staff set to True
def is_staff_user(user):
    return user.is_authenticated and user.is_staff


@login_required(login_url="authentication:login")
@user_passes_test(is_staff_user)
def create_new_user(request):
    if request.method == "POST":
        # Fetch User Details from Web Page
        fullname = request.POST.get("fullname")
        username = request.POST.get("username")
        password = request.POST.get("password")
        full_name = str(fullname).split(" ")

        first_name = full_name.pop(0)
        last_name = " ".join(full_name)

        try:
            # Create a New User instance and Set Attributes
            new_user = User.objects.create_user(username=username, password=password)
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.is_staff = False
            new_user.is_superuser = False

            # Save User to Database
            new_user.save()
            # Redirect User to Profile
            return redirect("authentication:show_user")

        # Catch the exception
        except Exception as ex:
            # Render Create User View and, Pass the Error Message to View
            return render(request, "create_user.html", {"error_message": str(ex)})

    # Render Initial Create User View
    return render(request, "create_user.html")


@login_required(login_url="authentication:login")
def create_user(request):
    # Render View
    return render(request, "create_user.html")


@login_required
def show_user(request):
    return render(
        request,
        "user.html",
        {
            "username": request.user.username,
            "password": request.user.password,
            "firstname": request.user.first_name,
        },
    )


@login_required
def logout_user(request):
    logout(request)
    return redirect("authentication:login")
