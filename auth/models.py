# IMPORTS
from django.db import models
from django.contrib.auth.models import User

# User Profile's can be used to modify the default User model, shipped with Django. 
# NOTICE: The field: 'first_name' already exists within Django I will use that rather than customizing the User Model Further...
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # favorite_food = models.CharField(max_length=125) # EXAMPLE CASE - NOT MIGRATED - DO NOT UNCOMMENT (UNLESS YOU MIGRATE)
