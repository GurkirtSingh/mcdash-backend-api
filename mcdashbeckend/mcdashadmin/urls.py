from django.urls import path
from .views import *

urlpatterns = [
    path('', admin_and_store_register, name='admin_and_store_register'),
    path('login', admin_login, name='admin_login'),
    path('home', admin_home, name='admin_home'),
    path('logout', admin_logout, name='admin_logout'),
    path('change-shift', assign_new_shift_view, name='assign_new_shift'),
]