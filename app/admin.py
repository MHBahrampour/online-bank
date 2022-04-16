from django.contrib import admin
from .models import Person, BankAccount


class PersonAdmin(admin.ModelAdmin):
	list_display = (
    'nid_number', 'first_name', 'last_name', 'date_of_birth', 
    'fathers_name', 'address', 'landline', 'zip_code'
  )
	search_fields = ('nid_number', 'first_name', 'last_name', 'address', 'zip_code')

class BankAccountAdmin(admin.ModelAdmin):
	list_display = (
    'nid_number', 'account_number', 'atm_card',
    'cvv2', 'expire_date', 'credit'
  )
	search_fields = ('nid_number', 'account_number', 'atm_card')


admin.site.register(Person, PersonAdmin)
admin.site.register(BankAccount, BankAccountAdmin)