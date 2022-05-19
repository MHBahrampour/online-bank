from django.db import models
from django.urls import reverse


class Person(models.Model):

  nid_number    = models.CharField(primary_key=True, max_length=10)

  first_name    = models.CharField(max_length=100)
  last_name     = models.CharField(max_length=100)
  fathers_name  = models.CharField(max_length=100)
  date_of_birth = models.DateField()

  address       = models.CharField(max_length=1024)
  landline      = models.CharField(max_length=11)
  zip_code      = models.CharField(max_length=10)

  def __str__(self):
    return self.nid_number


class BankAccount(models.Model):

  nid_number      = models.ForeignKey('Person', on_delete = models.CASCADE)

  atm_card        = models.CharField(max_length=16)
  account_number  = models.CharField(max_length=13)
  cvv2            = models.CharField(max_length=4)
  expire_date     = models.DateField()

  credit          = models.DecimalField(max_digits=19, decimal_places=10)

  def __str__(self):
    return self.account_number


class Transaction(models.Model):

  TYPE_CHOICES = [
    ('Transfer', 'Transfer'),
    ('Recharge', 'Recharge'),
    ('Charity', 'Charity'),
  ]

  type        = models.CharField(max_length=8, choices=TYPE_CHOICES)
  
  sender      = models.CharField(max_length=16)
  recipient   = models.CharField(max_length=16)

  amount      = models.CharField(max_length=12)

  date_time   = models.DateTimeField(auto_now_add=True)
  description = models.CharField(max_length=50, blank=True)

  rem_credit  = models.DecimalField(max_digits=19, decimal_places=10)

  # def get_to_card(self):

  #   # If the transaction type is Charity, return the institute name
  #   if self.type == 'CH':
  #     if self.to_card == '1':
  #       return "Mahak Institute"
  #     elif self.to_card == '2':
  #       return "Special Diseases"
  #     else:
  #       return "Child Foundation"

  #   # If the transaction type is Recharge, return the company name
  #   if self.type == 'RE':
  #     if self.to_card == '1':
  #       return "Irancell"
  #     elif self.to_card == '2':
  #       return "Hamrah Avval"
  #     else:
  #       return "Rightel"

  #   # If the transaction type is Transfer, return card number
  #   return self.to_card

  def __str__(self):
    return f"Transfer {self.amount}$ from {self.sender} to {self.recipient}."

  def get_absolute_url(self):
    return reverse('app:transaction_detail', args=[str(self.id)])
