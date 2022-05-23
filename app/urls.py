from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
  # Index page (Dashboard)
  path('', views.index, name='index'),

  path('dashboard/', views.dashboard, name='dashboard'),
  path('profile/', views.profile, name='profile'),

  path('transfer/', views.transfer, name='transfer'),
  path('recharge/', views.recharge, name='recharge'),
  path('charity/', views.charity, name='charity'),

  path('transactions/', views.transactions, name='transactions'),
  path('transactionDetail/<int:pk>/', views.transactionDetail, name='transaction_detail'),
]
