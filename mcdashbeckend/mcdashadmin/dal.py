from django.contrib.auth.models import User
from .models import Store, Staff, Employee, Shift, Shift_Detail, Previous_Shift_Detail
import datetime as dt

def get_all_usernames():
    usernames = []
    # get all usernames from database
    users = User.objects.all()
    for user in users:
        usernames.append(user.username)
    return usernames

def get_shift_detail_by_date(start_date):
    shifts = []
    # get all the shift object by date
    upcoming_shifts = Shift.objects.filter(shift_detail__start_at__date = start_date)
    for shift in upcoming_shifts:
        # query shift_details by shift
        shift_detail = Shift_Detail.objects.get(shift=shift)
        # get employee username
        user = shift.employee.user
        username = user.username
        # appand list
        shifts.append((username,shift_detail, shift.id))
    return shifts

def add_new_shift(user_name, start, end, station, storename):
    #step 1. find the employe with given 'username'
    user = User.objects.get(username=user_name)
    if user is None:
        print('User not found:- ' + user_name)
        return False
    emp = Employee.objects.get(user=user)
    if emp is None:
        print('Employee not found:- ' + user_name)
        return False
    #step 2. find store
    store_loc = Store.objects.get(name=storename)
    #step 3. create a new shift_detail object
    new_shift_detail = Shift_Detail.objects.create(
        start_at = start,
        end_at = end,
        station = station,
        store = store_loc
    )
    #step 4. create new 'shift' object with employee and shift_detail
    new_shift = Shift.objects.create(
        employee = emp,
        shift_detail = new_shift_detail
    )
    #step 5. return
    print('New Shift Addedd! :- '+ user_name)
    return True