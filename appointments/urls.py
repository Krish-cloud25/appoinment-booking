from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Appointment booking
    path('book/', views.book_appointment, name='book'),

    # Admin view
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/<int:pk>/', views.edit_appointment, name='edit_appointment'),
    path('delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),

    # 👇 Patient-level appointment CRUD
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('my-appointments/edit/<int:pk>/', views.edit_my_appointment, name='edit_my_appointment'),
    path('my-appointments/delete/<int:pk>/', views.delete_my_appointment, name='delete_my_appointment'),
]
