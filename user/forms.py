from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import CustomUser
from app.models import Person, BankAccount


# Registeration form
class CustomUserCreationForm(UserCreationForm):

  username      = forms.CharField(min_length=3, max_length=20)
  phone_number  = forms.CharField(min_length=11, max_length=11)
  nid_number    = forms.CharField(min_length=10, max_length=10)
  atm_card      = forms.CharField(min_length=16, max_length=16)

  class Meta:
    model   = CustomUser
    fields  = ('username', 'phone_number', 'nid_number', 'atm_card', 'password1', 'password2')
  
  # Validating fields
  def clean_username(self):

    username = self.cleaned_data['username']

    # Check that the username has not been used before
    try:
      username = CustomUser.objects.exclude(pk=self.instance.pk).get(username=username)
    except CustomUser.DoesNotExist:
      return username
    else:
      raise forms.ValidationError("Username is already in use.")
  
  def clean_phone_number(self):
    
    phone_number = self.cleaned_data['phone_number']

    # Check that the phone_number is correct (a number)
    try:
      int(phone_number)
    except ValueError:
      raise forms.ValidationError("Please enter a correct Phone number. It should be contain only digits.")

    return phone_number

  def clean_nid_number(self):

    nid_number = self.cleaned_data['nid_number']

    # Check that the nid_number is correct (a number)
    try:
      int(nid_number)
    except ValueError:
      raise forms.ValidationError("Please enter a correct NID number. It should be contain only digits.")

    # Check that the nid_number registered in Person table
    try:
      Person.objects.get(nid_number=nid_number)
    except Person.DoesNotExist:
      raise forms.ValidationError("There is no account with this NID number in the bank.")

    return nid_number

  def clean_atm_card(self):

    atm_card = self.cleaned_data['atm_card']

    # Check that the atm_card is correct (a number)
    try:
      int(atm_card)
    except ValueError:
      raise forms.ValidationError("Please enter a correct NID number. It should be contain only digits.")

    # Check that the atm_card registered in BankAccount table
    try:
      BankAccount.objects.get(atm_card=atm_card)
    except BankAccount.DoesNotExist:
      raise forms.ValidationError("There is no account with this ATM card in the bank.")

    # Check that atm_card is not already in use
    try:
      atm_card = CustomUser.objects.exclude(pk=self.instance.pk).get(atm_card=atm_card)
    except CustomUser.DoesNotExist:
      return atm_card
    else:
      raise forms.ValidationError("ATM card is already in use.")
    

# Authentication form
class CustomUserAuthenticationForm(forms.ModelForm):

  password = forms.CharField(label='Password', widget=forms.PasswordInput)

  class Meta:
    model   = CustomUser
    fields  = ('username', 'password')

  # Validating fields
  def clean(self):
    if self.is_valid():
      username = self.cleaned_data['username']
      password = self.cleaned_data['password']
      
      if not authenticate(username=username, password=password):
        raise forms.ValidationError("Invalid login")
