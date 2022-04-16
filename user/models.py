from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser):

  username      = models.CharField(max_length=20, unique=True)

  phone_number  = models.CharField(max_length=11)
  # National ID Number
  nid_number    = models.CharField(max_length=10)
  # ATM card
  atm_card      = models.CharField(max_length=16)

  is_admin			= models.BooleanField(default=False)
  is_staff      = models.BooleanField(default=False)
  is_superuser  = models.BooleanField(default=False)
  is_active     = models.BooleanField(default=True)

  date_joined		= models.DateTimeField(auto_now_add=True)
  last_login		= models.DateTimeField(auto_now=True)

  USERNAME_FIELD  = 'username'
  REQUIRED_FIELDS = ['phone_number', 'nid_number', 'atm_card']

  objects = CustomUserManager()

  def __str__(self):
    return self.username

  # For checking permissions. to keep it simple all admin have ALL permissons
  def has_perm(self, perm, obj=None):
    return self.is_admin

  # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
  def has_module_perms(self, app_label):
    return True