from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, DateTimeField
from django.contrib.auth.models import User
from .models import Previous_Shift_Detail, Shift, Shift_Detail, Store, Staff

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

# form to assign a new shift
class assign_new_shift(ModelForm):
    shift_id = CharField(max_length=10)
    store_name = CharField(max_length=100)
    class Meta:
        model = Shift_Detail
        fields = ['start_at', 'end_at', 'station', 'store_name', 'shift_id']

    def clean(self):
        cleaned_data = super().clean()
        shift = Shift.objects.get(pk=cleaned_data['shift_id'])
        if shift is None:
            raise ValidationError({'shift_id': 'shift does not exists!'})
        store = Store.objects.get(name=cleaned_data['store_name'])
        if store is None:
            raise ValidationError({'store_name': 'store does not exists!'})
        return cleaned_data

    def save(self, commit=False):
        instance = super().save(commit=commit)
        # get shift obj
        shift = Shift.objects.get(pk=self.cleaned_data['shift_id'])
        # add current shift details to prev
        Previous_Shift_Detail.objects.create(
            shift=shift,
            shift_detail = shift.shift_detail
        )
        # get store by name
        store = Store.objects.get(name=self.cleaned_data['store_name'])
        instance.store = store
        instance.save(True)
        # assign new shift details to shift
        shift.shift_detail = instance
        shift.save()
        return instance