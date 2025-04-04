from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('appointments.urls')),  # 👈 this line connects to your app
]
