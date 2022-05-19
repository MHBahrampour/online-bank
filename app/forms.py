from django import forms
from decimal import Decimal

from user.models import CustomUser
from .models import BankAccount


class TransferForm(forms.Form):

  def __init__(self, *args, **kwargs):
    self.request = kwargs.pop("request") # store value of request 
    print(self.request.user) 
    super().__init__(*args, **kwargs)
  
  recipient   = forms.CharField(label='Destination Card', min_length=16, max_length=16)

  amount      = forms.CharField(label='Amount', max_length=12)
  description = forms.CharField(label='Description', max_length=50, required=False)

  cvv2        = forms.CharField(label='CVV2', min_length=4, max_length=4)
  second_pass = forms.CharField(label='Second Password', widget=forms.PasswordInput)

  # Validating fields (todo)
  def clean_recipient(self):
    
    recipient = self.cleaned_data['recipient']

    # Check that the recipient card is correct (a number)
    try:
      int(recipient)
    except ValueError:
      raise forms.ValidationError("Please enter a correct Card Number. It should be contain only digits.")

    # Check that the recipient card is for a real bank
    if not ( recipient[:6] in ('603799', '589210', '627648') ):
      raise forms.ValidationError("Please enter a correct Card Number. This card number does not belong to any bank.")

    return recipient

  def clean_amount(self):
    
    amount = Decimal(self.cleaned_data['amount'])

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

class CharityForm(forms.Form):

  CHARITY_CHOICES = (
    ('', "Nothing Selected"),
    ('Mahak Institute', "Mahak Institute"),
    ('Special Diseases', "Special Diseases"),
    ('Child Foundation', "Child Foundation")
  )

  charity     = forms.ChoiceField(label='Charity', choices = CHARITY_CHOICES)
  amount      = forms.CharField(label='Amount', max_length=12)
  description = forms.CharField(label='Description', max_length=50, required=False)

  # Validating fields (todo)

class RechargeForm(forms.Form):

  COMPANY_CHOICES = (
    ('', "Nothing Selected"),
    ('Irancell', "Irancell"),
    ('Hamrahe Avval', "Hamrahe Avval"),
    ('Rightel', "Rightel")
  )

  CHARGE_CHOICES = (
    ('', "Nothing Selected"),
    ('10_000', "10_000"),
    ('20_000', "20_000"),
    ('50_000', "50_000"),
    ('100_000', "100_000"),
    ('200_000', "200_000"),
  )

  company       = forms.ChoiceField(label='Company', choices = COMPANY_CHOICES)
  mobile_number = forms.CharField(label='Mobile Number', min_length=11, max_length=11)
  charge_amount = forms.ChoiceField(label='Charge amount', choices = CHARGE_CHOICES)
  description   = forms.CharField(label='Description', max_length=50, required=False)

  # Validating fields (todo)