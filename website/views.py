from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import *
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in" )
            return redirect('home')
        else:
            messages.success(request, "Error logging in")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records':records})

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out")
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "User Registered")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html',{'form': form})
    return render(request, 'register.html',{'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, "You must be Logged in")
        return redirect('home')

def delete_record(request,pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        customer_record.delete()
        messages.success(request, "Record Deleted")
        return redirect('home')
    else:
        messages.success(request, "You must be Logged in")
        return redirect('home')

def add_record(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email =  request.POST.get('email')
        phone = request.POST.get('phone') 
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        new_record = Record(first_name=first_name, last_name=last_name, email=email, phone=phone, address=address, city=city, state=state, zipcode=zipcode)
        new_record.save()
        messages.success(request, "Record Saved Successfully!")
        return redirect('home')
    return render(request, 'add_record.html')

def update_record(request, pk):
    record= Record.objects.get(id=pk)
    if request.method == 'POST':
        record.first_name = request.POST.get('first_name')
        record.last_name = request.POST.get('last_name')
        record.email =  request.POST.get('email')
        record.phone = request.POST.get('phone') 
        record.address = request.POST.get('address')
        record.city = request.POST.get('city')
        record.state = request.POST.get('state')
        record.zipcode = request.POST.get('zipcode')
        record.save()
        return redirect('home')
    return render(request, 'update_record.html', {'record':record})