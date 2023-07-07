from django.contrib import admin
from .models import User, Profile
from django.contrib.auth import get_user_model

# Register your models here.


User = get_user_model()

# Unregister the User model from the admin site if it's already registered
if admin.site.is_registered(User):
    admin.site.unregister(User)

# Register the User model with a custom admin class
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    # Customize the admin options for the User model if needed
    pass

admin.site.register(Profile)