from django.urls import path
from .views import admin_and_store_register, admin_login, admin_home

urlpatterns = [
    path('', admin_and_store_register, name='admin_and_store_register'),
    path('/login', admin_login, name='admin_login'),
    path('/home', admin_home, name='admin_home'),
]