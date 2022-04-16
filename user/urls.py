from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    # Register, Login and Logout urls
    path('register/',   views.registerUser,  name='register' ),
    path('login/',      views.loginUser,     name='login'    ),
    path('logout/',     views.logoutUser,    name='logout'   ),
]