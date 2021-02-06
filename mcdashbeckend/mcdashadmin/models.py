from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.db.models.fields import DateTimeField

# STORE - Model
class Store(models.Model):
    store_number = models.CharField(max_length=100, unique=True) # store id or uniqly identified number
    name = models.CharField(max_length=100)

# Staff - Model
class Staff(models.Model):
    store = models.ForeignKey(Store, on_delete=CASCADE)
    is_admin = models.BooleanField(default=False)
    position = models.CharField(max_length=100, blank=False)

# SHIFT_DETAIL - Model
class Shift_Detail(models.Model):
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    station = models.CharField(max_length=30)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

# Employee - Model
class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=CASCADE)

# Shift - model
class Shift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=CASCADE)
    shift_detail = models.ForeignKey(Shift_Detail, on_delete=CASCADE)

class Previous_Shift_Detail(models.Model):
    shift = models.ForeignKey(Shift, on_delete=CASCADE)
    shift_detail = models.ForeignKey(Shift_Detail, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)