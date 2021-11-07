from django.http import JsonResponse
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import StoreForm, UserForm, assign_new_shift
from .models import Shift, Shift_Detail, Staff, Employee
from .services import scan_schedule_from_pdf
from .dal import get_all_usernames, get_shift_detail_by_date
import datetime as dt
import json
from rest_framework.response import Response

# Create your views here.
def admin_and_store_register(req):
    context = {}
    if req.method == 'POST':

        # get forms data from post request
        # storeForm, employeeForm, staffForm
        store_form = StoreForm(req.POST, prefix='storeform')
        user_form = UserForm(req.POST, prefix='employeeform')
        # currently staff position not getting from user
        # assuming admin is a schedule manager
        staff_position = "Schedule Manager"

        # validate forms data
        if store_form.is_valid() and user_form.is_valid():
            # if all the forms contain valid data
            # create store by saving storeForm
            store = store_form.save()

            # create user by saving userForm
            # save encrypted password
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()


            # create staff by staffForm.position and linking with store
            # also make is admin to true
            staff, _ = Staff.objects.get_or_create(
                    position=staff_position,
                    store=store,
                    is_admin = True
                    )

            # finally create emplyee
            # by linking user and store
            if staff is not None:
                new_employee, _ = Employee.objects.get_or_create(
                    user=user,
                    staff=staff
                )
                if new_employee is not None:
                    return redirect('admin_home')
                else:
                    context['page_error'] = 'Unable to create employee'
            else:
                context['page_error'] = 'Unable to create staff position'
        else:
            context['store_form'] = store_form
            context['employee_form'] = user_form
    else:
        context['store_form'] = StoreForm(prefix='storeform')
        context['employee_form'] = UserForm(prefix='employeeform')
    return render(req, 'mcdashadmin/landingPage.html', context)    

# login view
def admin_login(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(req, username=username, password=password)
        if user is not None:
            # check if user is a admin
            employee = Employee.objects.get(user=user)
            if employee is not None:
                if employee.staff.is_admin:
                    login(req, user)
                    # Redirect to a success page.
                    return redirect('admin_home')      
        else:
            empty_store_form = StoreForm(prefix='storeform')
            empty_employee_form = UserForm(prefix='employeeform')
            context = {
                'store_form': empty_store_form,
                'employee_form': empty_employee_form,
                'loginError' : "Admin's username/password is invalid",
            }
            # Return an 'invalid login' error message.
            return render(req, 'mcdashadmin/landingPage.html', context=context)
    else:
        return redirect('admin_and_store_register')

# home page
@login_required(login_url='admin_login')
def admin_home(req):
    # check if the user is admin
    employee = Employee.objects.get(user=req.user)
    if not employee.staff.is_admin:
        return HttpResponse(HttpResponseBadRequest)
    context = {}
    context['shifts'] = get_shift_detail_by_date(dt.date(2021, 1, 11))
    if req.method == 'POST':
        file = req.FILES['sche-pdf']
        if file is not None:
            if file.content_type == 'application/pdf': # 
                # if the slected file is a valid 'pdf' format
                # send it to scan schedule
                scan_schedule_from_pdf(file)
                context['success'] = 'Uploaded Successfuly!'
            else:
                context['error'] = 'Please select a pdf file!'
        else:
            context['error'] = 'Please select a file!'
    return render(req, 'mcdashadmin/adminhome.html', context)

# logout
@login_required(login_url='admin_login')
def admin_logout(req):
    logout(request=req)
    return redirect('admin_and_store_register')

# assign new shift
@login_required(login_url='admin_login')
def assign_new_shift_view(req):
    if req.method != 'POST':
        return HttpResponse(HttpResponseNotAllowed)
    data = {}
    new_form = assign_new_shift(req.POST)
    if new_form.is_valid():
        new_form.save()
        data['response'] = 'New Shift assigned succesfully!'
    else:
        data = new_form.errors
    return JsonResponse(data)