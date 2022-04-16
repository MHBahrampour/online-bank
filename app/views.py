from django.shortcuts import render
from .models import Person, BankAccount
from user.models import CustomUser


def index(request):

  context = {
    'str1': "Hi, I'm a useless bank application!",
    'str2': "Just for now.",
    'username': request.user,
  }

  return render(request, 'index.html', context)

def profile(request):

  user_data = CustomUser.objects.get(username=request.user)
  person_data = Person.objects.get(nid_number=user_data.nid_number)
  bank_account_data = BankAccount.objects.get(atm_card=user_data.atm_card)

  context = {
    # User Data
    'username': user_data.username,
    'phone_number': user_data.phone_number,
    'date_joined': user_data.date_joined,

    # Personal Data
    'first_name': person_data.first_name,
    'last_name': person_data.last_name,
    'fathers_name': person_data.fathers_name,
    'date_of_birth': person_data.date_of_birth,
    'address': person_data.address,
    'landline': person_data.landline,
    'zip_code': person_data.zip_code,
    
    # Bank Account Data
    'account_number': bank_account_data.account_number,
    'atm_card': bank_account_data.atm_card,
    'cvv2': bank_account_data.cvv2,
    'expire_date': bank_account_data.expire_date,
  }

  return render(request, 'profile.html', context)