from django.core.exceptions import ValidationError
from django.forms import ModelForm, fields
from django.contrib.auth.models import User
from .models import Store, Staff

# StoreForm
class StoreForm(ModelForm):
    class Meta:
        model = Store
        fields = ['store_number', 'name']

# Userform
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
