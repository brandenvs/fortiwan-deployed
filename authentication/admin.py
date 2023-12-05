# IMPORTS
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import StandardUser

# Custom UserProfile Model Called: UserProfile(default: see models.py)
class UserProfileInLine(admin.StackedInline):
    model = StandardUser
    can_delete = False
    verbose_name_plural = "admins"

# Class Inherits the BaseUserAdmin, which is UserAdmin within Django Framework
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInLine]

# Unregister the default User Model from Admin Dashboard
admin.site.unregister(User)
# Register User and the new UserAdmin* class
admin.site.register(User, UserAdmin)
