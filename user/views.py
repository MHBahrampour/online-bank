from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate

from .forms import CustomUserCreationForm, CustomUserAuthenticationForm


def registerUser(request):
  
  user = request.user
  if user.is_authenticated: 
    return HttpResponse(f"You are already authenticated as {user.username}")

  context = {}
  if request.POST:
    form = CustomUserCreationForm(request.POST)
    
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      raw_password = form.cleaned_data.get('password1')
      user = authenticate(request, username=username, password=raw_password)
      login(request, user)
      return redirect('app:index')

    else:
      context['registration_form'] = form

  # If the request type is GET
  else:
    form = CustomUserCreationForm()
    context['registration_form'] = form

  return render(request, 'register.html', context)

def loginUser(request):

  context = {}

  user = request.user
  if user.is_authenticated: 
    return redirect('app:index')

  if request.method == 'POST':
    form = CustomUserAuthenticationForm(request.POST)

    if form.is_valid():
      username = request.POST['username']
      password = request.POST['password']
      user = authenticate(request, username=username, password=password)

      if user:
        login(request, user)
        return redirect('app:index')

  else:
    form = CustomUserAuthenticationForm()

  context['login_form'] = form

  return render(request, "login.html", context)

def logoutUser(request):

	logout(request)
	return redirect('app:index')