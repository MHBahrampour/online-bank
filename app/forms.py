import re
from django import forms
from decimal import Decimal

from user.models import CustomUser
from .models import BankAccount


class TransferForm(forms.Form):

  def __init__(self, *args, **kwargs):
    self.request = kwargs.pop("request") # store value of request 
    super().__init__(*args, **kwargs)
  
  recipient   = forms.CharField(label='Destination Card', min_length=16, max_length=16)

  amount      = forms.CharField(label='Amount', max_length=19)
  description = forms.CharField(label='Description', max_length=50, required=False)

  cvv2        = forms.CharField(label='CVV2', min_length=4, max_length=4)
  second_pass = forms.CharField(label='Second Password', widget=forms.PasswordInput)

  # Validating fields
  def clean_recipient(self):
    
    recipient = self.cleaned_data['recipient']

    # Check that the recipient card is correct (a number)
    try:
      int(recipient)
    except ValueError:
      raise forms.ValidationError("Please enter a correct Card Number. It should be contain only digits.")

    # Check that the recipient card is for a real bank
    # Meli, Sepah, Tejarat, Maskan, Saman 
    if not ( recipient[:6] in ('603799', '589210', '627648', '628023', '621986') ):
      raise forms.ValidationError("This card number does not belong to any bank.")

    return recipient

  def clean_amount(self):
    
    amount = int( self.cleaned_data['amount'] )

    # Check that the minimum transfer amount is observed
    if amount < 10000:
      raise forms.ValidationError("The transfer amount must be at least 10,000 Rials.")

    # Check that the user has anough credit for this transfer
    user = self.request.user
    user_atm_card = CustomUser.objects.get(username=user.username).atm_card
    user_credit = BankAccount.objects.get(atm_card=user_atm_card).credit
    if user_credit < amount:
      raise forms.ValidationError("You don't have enough money in your card.")

    return amount

  def clean_cvv2(self):
    
    cvv2 = self.cleaned_data['cvv2']

    # Check that the user entered the correct CVV2
    user = self.request.user
    user_atm_card = CustomUser.objects.get(username=user.username).atm_card
    user_cvv2 = BankAccount.objects.get(atm_card=user_atm_card).cvv2
    if user_cvv2 != cvv2:
      raise forms.ValidationError("Enter the correct CVV2 number of your card.")

    return cvv2

  def clean_second_pass(self):
    
    second_pass = self.cleaned_data['second_pass']

    # Check that the user entered the correct Seccond Password
    if not ( second_pass in ('1', '2', '3', '4', '5', '6', '7', '8', '9') ):
      raise forms.ValidationError("Enter the correct Seccont Password of your card.")

    return second_pass

class RechargeForm(forms.Form):

  def __init__(self, *args, **kwargs):
    self.request = kwargs.pop("request") # store value of request 
    print(self.request.user) 
    super().__init__(*args, **kwargs)

  COMPANY_CHOICES = (
    ('', "Nothing Selected"),
    ('Irancell', "Irancell"),
    ('Hamrahe Avval', "Hamrahe Avval"),
    ('Rightel', "Rightel")
  )

  CHARGE_CHOICES = (
    ('', "Nothing Selected"),
    ('10000', "10,000"),
    ('20000', "20,000"),
    ('50000', "50,000"),
    ('100000', "100,000"),
    ('200000', "200,000"),
  )

  company       = forms.ChoiceField(label='Company', choices=COMPANY_CHOICES)
  mobile_number = forms.CharField(label='Mobile Number', min_length=11, max_length=11)
  charge_amount = forms.ChoiceField(label='Charge amount', choices=CHARGE_CHOICES)
  description   = forms.CharField(label='Description', max_length=50, required=False)

  # Validating fields
  def clean_mobile_number(self):

    pre_code = {
      'Irancell': ['0930', '0933', '0935', '0936', '0937', '0938', '0939', '0901', '0902', '0903', '0905'],
      'Hamrahe Avval': ['0990', '0991', '0992', '0993', '0994', '0911', '0912', '0913', '0914', '0915', '0916', '0917', '0918'],
      'Rightel': ['0920', '0921', '0922'],
    }

    mobile_number = self.cleaned_data['mobile_number']
    company       = self.cleaned_data['company']

    # Check that the Mobile Number is correct (a number)
    try:
      int(mobile_number)
    except ValueError:
      raise forms.ValidationError("Please enter a correct Mobile Number. It should be contain only digits.")

    # Check that the Mobile Number belong to the selected company
    if not mobile_number[:4] in pre_code[company]:
      raise forms.ValidationError("This number don't belong to the selected company.")

    return mobile_number

  def clean_charge_amount(self):

    charge_amount = int( self.cleaned_data['charge_amount'] )

    user = self.request.user
    user_atm_card = CustomUser.objects.get(username=user.username).atm_card
    user_credit = BankAccount.objects.get(atm_card=user_atm_card).credit
    amountPlusTax = charge_amount + ( 0.09 * charge_amount )

    if user_credit < amountPlusTax:
      raise forms.ValidationError("You don't have enough money in your card.")

    return charge_amount

class CharityForm(forms.Form):

  def __init__(self, *args, **kwargs):
    self.request = kwargs.pop("request") # store value of request 
    print(self.request.user) 
    super().__init__(*args, **kwargs)

  CHARITY_CHOICES = (
    ('', "Nothing Selected"),
    ('Mahak Institute', "Mahak Institute"),
    ('Special Diseases', "Special Diseases"),
    ('Child Foundation', "Child Foundation")
  )

  charity     = forms.ChoiceField(label='Charity', choices=CHARITY_CHOICES)
  amount      = forms.CharField(label='Amount', max_length=19)
  description = forms.CharField(label='Description', max_length=50, required=False)

  # Validating fields
  def clean_amount(self):

    amount = int(self.cleaned_data['amount'])

    user = self.request.user
    user_atm_card = CustomUser.objects.get(username=user.username).atm_card
    user_credit = BankAccount.objects.get(atm_card=user_atm_card).credit

    if user_credit < amount:
      raise forms.ValidationError("You don't have enough money in your card.")

    return amount
