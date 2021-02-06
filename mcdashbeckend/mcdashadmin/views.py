from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import StoreForm, UserForm
from .models import Staff, Employee

# Create your views here.
def admin_and_store_register(req):
    if req.method == 'POST':

        # get forms data from post request
        # storeForm, employeeForm, staffForm
        store_form = StoreForm(req.POST, prefix='storeform')
        user_form = UserForm(req.POST, prefix='employeeform')
        staff_position = req.POST['staff_position']

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
            staff, created = Staff.objects.get_or_create(
                    position=staff_position,
                    store=store,
                    is_admin = True
                    )

            # finally create emplyee
            # by linking user and store
            if staff is not None:
                new_employee, created = Employee.objects.get_or_create(
                    user=user,
                    staff=staff
                )
                if new_employee is not None:
                    # if employee regitered successfully
                    # log on console
                    # redirect to a Thank you page or home page

                    # save all the models
                    print('New store is registered.')
                    print('Store Number: ' + store.store_number)
                    print('Admin: ' + new_employee.user.username)
                    print('------------------------')
                    context = {
                        'store_name' : store_form.cleaned_data['name'],
                    }
                    return redirect('admin_home')
                else:
                    return render(req, 'mcdashadmin/ServerError.html')
            else:
                return render(req, 'mcdashadmin/ServerError.html')
        else:
            context = {
                'store_form' : store_form,
                'employee_form': user_form,
            }
            return render(req, 'mcdashadmin/splash.html', context)
    else:
        empty_store_form = StoreForm(prefix='storeform')
        empty_employee_form = UserForm(prefix='employeeform')
        content = {
            'store_form': empty_store_form,
            'employee_form': empty_employee_form,
        }
        return render(req, 'mcdashadmin/splash.html', context=content)

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
            return render(req, 'mcdashadmin/splash.html', context=context)
    else:
        return redirect('admin_and_store_register')

# home page
@login_required(login_url='login')
def admin_home(req):
    return render(req, 'mcdashadmin/adminhome.html')