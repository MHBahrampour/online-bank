from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
	list_display = (
    'username', 
    'phone_number', 'nid_number', 'atm_card', 
    'is_admin','is_staff', 
    'date_joined', 'last_login'
  )
	search_fields = ('username', 'nid_number', 'atm_card')
	readonly_fields = ('date_joined', 'last_login', 'password')


admin.site.register(CustomUser, CustomUserAdmin)