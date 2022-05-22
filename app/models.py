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

  credit          = models.PositiveBigIntegerField()

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

  amount      = models.PositiveBigIntegerField()

  date_time   = models.DateTimeField(auto_now_add=True)
  description = models.CharField(max_length=50, blank=True)

  rem_credit  = models.PositiveBigIntegerField()

  def __str__(self):
    return f"Transfer {self.amount}$ from {self.sender} to {self.recipient}."

  def get_absolute_url(self):
    return reverse('app:transaction_detail', args=[str(self.id)])
