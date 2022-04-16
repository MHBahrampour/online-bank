from django.db import models

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

  account_number  = models.CharField(max_length=13)
  atm_card        = models.CharField(max_length=16)
  cvv2            = models.CharField(max_length=4)
  expire_date     = models.DateField()

  credit          = models.CharField(max_length=12)

  def __str__(self):
    return self.account_number