from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q

from .models import Person, BankAccount, Transaction
from user.models import CustomUser
from .forms import TransferForm, RechargeForm, CharityForm



def index(request):

  if request.user.is_authenticated:
    return redirect('app:dashboard')

  return render(request, 'index.html')


def dashboard(request):

  if not request.user.is_authenticated:
    return redirect('app:app')

  return render(request, 'app/dashboard.html')


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

  return render(request, 'app/profile.html', context)


def transfer(request):

  # Define context dictionary to be filled in the process
  context = {}
  
  # Get User model of the current user 
  user = request.user

  # Check if the user is not authenticated
  if not user.is_authenticated:
    return HttpResponse("You have to login first.")

  # User card number
  sender = CustomUser.objects.get(username=user.username).atm_card

  # If the request type is POST
  if request.POST:

    # Create the respective Form with a POST request
    form = TransferForm(request.POST, request=request)

    # Check if the form passed verifications
    if form.is_valid():

      # Reduce the amount from the sender
      amount = form.cleaned_data.get('amount')
      sender_bank_account_data = BankAccount.objects.get(atm_card=sender)

      sender_bank_account_data.credit -= amount
      sender_bank_account_data.save() # Save the change (credeit value)

      # Add the amount to the recipient
      # Here we need a 'try except' block because the recipient may not be in our app
      recipient = form.cleaned_data.get('recipient')
      try:
        recipient_bank_account_data = BankAccount.objects.get(atm_card=recipient)
      except BankAccount.DoesNotExist:
        pass
      else:
        recipient_bank_account_data.credit += amount
        recipient_bank_account_data.save() # Save the change (credeit value)

      # Create and save the Transaction instance
      transaction = Transaction.objects.create(
        type = 'Transfer',
        sender = sender,
        recipient = recipient,
        amount = amount,
        description = form.cleaned_data.get('description'),
        rem_credit = sender_bank_account_data.credit,
      )

      # Redirect user to the TransactionDetail page
      return redirect('app:transaction_detail', pk=transaction.id)

    # If form wasn't valid, return unvalid form to be filled again
    else:
      context['transaction_form'] = form

  # If the request type is GET, create an empty form and pass it to template
  else:
    form = TransferForm(request=request)
    context['transaction_form'] = form
  
  context['sender'] = sender

  return render(request, 'app/transfer.html', context)


def recharge(request):

  # Define context dictionary to be filled in the process
  context = {}
  
  # Get User model of the current user 
  user = request.user

  # Check if the user is not authenticated
  if not user.is_authenticated:
    return HttpResponse("You have to login first.")

  # User card number
  sender = CustomUser.objects.get(username=user.username).atm_card

  # If the request type is POST
  if request.POST:

    # Create the respective Form with a POST request
    form = RechargeForm(request.POST, request=request)

    # Check if the form passed verifications
    if form.is_valid():

      # Reduce the amount from the sender
      amount = form.cleaned_data.get('charge_amount')
      tax = 0.09 * amount
      amountPlusTax = amount + tax
      sender_bank_account_data = BankAccount.objects.get(atm_card=sender)

      sender_bank_account_data.credit -= amount
      sender_bank_account_data.save() # Save the change (credeit value)

      # Create and save the Transaction instance
      transaction = Transaction.objects.create(
        type = 'Recharge',
        sender = sender,
        recipient = form.cleaned_data.get('company'),
        amount = amountPlusTax,
        description = form.cleaned_data.get('description'),
        rem_credit = sender_bank_account_data.credit,
      )

      # Redirect user to the TransactionDetail page
      return redirect('app:transaction_detail', pk=transaction.id)

    # If form wasn't valid, return unvalid form to be filled again
    else:
      context['recharge_form'] = form

  # If the request type is GET, create an empty form and pass it to template
  else:
    form = RechargeForm(request=request)
    context['recharge_form'] = form

  return render(request, 'app/recharge.html', context)


def charity(request):

  # Define context dictionary to be filled in the process
  context = {}
  
  # Get User model of the current user 
  user = request.user

  # Check if the user is not authenticated
  if not user.is_authenticated:
    return HttpResponse("You have to login first.")

  # User card number
  sender = CustomUser.objects.get(username=user.username).atm_card

  # If the request type is POST
  if request.POST:

    # Create the respective Form with a POST request
    form = CharityForm(request.POST, request=request)

    # Check if the form passed verifications
    if form.is_valid():

      # Reduce the amount from the sender
      amount = form.cleaned_data.get('amount')
      sender_bank_account_data = BankAccount.objects.get(atm_card=sender)

      sender_bank_account_data.credit -= amount
      sender_bank_account_data.save() # Save the change (credeit value)

      # Create and save the Transaction instance
      transaction = Transaction.objects.create(
        type = 'Charity',
        sender = sender,
        recipient = form.cleaned_data.get('charity'),
        amount = amount,
        description = form.cleaned_data.get('description'),
        rem_credit = sender_bank_account_data.credit,
      )

      # Redirect user to the TransactionDetail page
      return redirect('app:transaction_detail', pk=transaction.id)

    # If form wasn't valid, return unvalid form to be filled again
    else:
      context['charity_form'] = form

  # If the request type is GET, create an empty form and pass it to template
  else:
    form = CharityForm(request=request)
    context['charity_form'] = form
      
  return render(request, 'app/charity.html', context)


def transactions(request):

  # User card number
  user_card = CustomUser.objects.get(username=request.user.username).atm_card

  # All user transactions
  transactions = Transaction.objects.filter( Q(sender=user_card) | Q(recipient=user_card) ).order_by('-date_time')

  context = { 
    'transactions': transactions, 
    'user_card': user_card,
  }

  return render(request, 'app/transactions.html', context)


def transactionDetail(request, pk):

  transaction = Transaction.objects.get(pk=pk)

  # User card number
  user_card = CustomUser.objects.get(username=request.user.username).atm_card

  context = {
    'transaction': transaction,
    'user_card': user_card,
  }

  return render(request, 'app/transaction_detail.html', context)
