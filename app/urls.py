from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
  # Index page (Dashboard)
  path('', views.index, name='index'),
  path('profile/', views.profile, name='profile'),
]
