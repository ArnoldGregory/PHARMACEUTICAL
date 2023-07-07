from django.db import models
#from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    name = models.CharField(max_length=100)
    pharmacist = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.pharmacist} - Profile'
    # fields and methods in your custom User model
