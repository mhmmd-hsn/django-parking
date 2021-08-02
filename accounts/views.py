from django.contrib.auth.models import Group
from django.shortcuts import render,redirect
import time
from .forms import *
from .filters import SLotFilter

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required



from .decorators import unauthenticated_user, allowed_users, admin_only


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    slots_inf = Slot.objects.order_by('-id')[:5]
    customers = Customer.objects.order_by('-id')[:5]
    capacity = Capacity.objects.last()
    enters = Slot.objects.filter(event_type='Enter').count()
    exits = Slot.objects.filter(event_type='Exit').count()
    busy_slots = enters - exits
    free_slots = capacity.capacity - busy_slots
    context = {'slots_inf': slots_inf,
               'customers': customers,
               'capacity': capacity,
               'Enters': enters,
               'Exits': exits,
               'busy_slots': busy_slots,
               'free_slots': free_slots}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    customer_activities = request.user.customer.slot_set.all()
    customer = request.user.customer
    total_enters = request.user.customer.slot_set.filter(event_type='Enter').count()
    context = {'customer_activities': customer_activities, 'customer': customer, 'total_enters': total_enters}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def customer(request, pk_test):
    customer = Customer.objects.get(id= pk_test)
    customer_activities = customer.slot_set.all()

    myFilter = SLotFilter(request.GET, queryset=customer_activities)
    customer_activities = myFilter.qs
    enters = customer_activities.filter(event_type='Enter').count()
    exits = customer_activities.filter(event_type='Exit').count()
    if enters - exits == 1:
        status = 'you are in parking'
    else:
        status = 'you are outside'
    activity_count = customer_activities.count()

    context = {'customer': customer,
               'customer_activities': customer_activities,
               'activity_count': activity_count,
               'status': status,
               'myFilter': myFilter}

    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def ChangeCapacity(request):
    form = Change_Capacity()
    if request.method == 'POST':
        form = Change_Capacity(request.POST)
        if form.is_valid():
            form.save()
            extra_slots = Capacity.objects.last()
            num_of_last_slots_id = extra_slots.id - 1
            last_slots = Capacity.objects.get(id=num_of_last_slots_id)
            new_capacity = last_slots.capacity + extra_slots.capacity
            p = Capacity(capacity=new_capacity)
            p.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/capacity.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def CreateEvent(request, pk):
    customer = Customer.objects.get(id=pk)
    capacity = Capacity.objects.last()
    last_activity = Slot.objects.filter(customer=customer).last()
    for slot_num in range(1, capacity.capacity + 1):
        slot_activities = Slot.objects.filter(slot_num=slot_num).count()
        x = slot_activities % 2
        if x == 0:
            slot_number = slot_num
            break
        #parking be full
        if slot_num == capacity.capacity:
            time.sleep(2)
            return redirect('/')
        #already be inside
        if last_activity != None and last_activity.event_type == 'Enter':
            time.sleep(2)
            return redirect('/')

    if request.method == "POST":
        p = Slot(customer=customer, event_type='Enter', slot_num=slot_number)
        p.save()
        return redirect('/')

    context = {'customer': customer}
    return render(request, 'accounts/enter_confirm.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def ExitEvent(request, pk):
    customer = Customer.objects.get(id=pk)
    slot_inf = Slot.objects.filter(customer=customer).last()
    last_activity = Slot.objects.filter(customer=customer).last()
    if last_activity == None or last_activity.event_type == 'Exit' :
            time.sleep(2)
            return redirect('/')

    if request.method == "POST":
        p = Slot(customer=customer, event_type='Exit', slot_num=slot_inf.slot_num)
        p.save()
        return redirect('/')
    context = {'customer': customer}
    return render(request, 'accounts/exit_confirm.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def DeleteEvent(request, pk):
    item = Slot.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect('/')
    context = {'item': item}
    return render(request, 'accounts/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)



@login_required(login_url='login')
@admin_only
def ParkingData(request):
    all_activities = Slot.objects.all()
    context = {'all_activities': all_activities}
    return render(request, 'accounts/parking_data.html', context)


@login_required(login_url='login')
@admin_only
def AllCustomers(request):
    all_customers = Customer.objects.all()
    context = {'all_customers': all_customers}
    return render(request, 'accounts/all_customers.html', context)


@login_required(login_url='login')
@admin_only
def SetAsAdmin(request ,pk):
    customer =Customer.objects.get(id=pk)
    group =  Group.objects.get(name='admin')
    user = User.objects.get(username = customer.name)
    if request.method == "POST":
        user.groups.add(group)
        user.is_staff = True
        return redirect('/')
    context = {'customer' :customer , 'user':user}
    return render(request, 'accounts/set_as_admin.html', context)