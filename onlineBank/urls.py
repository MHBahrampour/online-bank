from django.contrib import admin
from django.urls import path, include


urlpatterns = [
  # Admin site
  path('admin/', admin.site.urls),
  
  # Including apps urls
  path('app/', include('app.urls')),
  path('user/', include('user.urls')),
]
