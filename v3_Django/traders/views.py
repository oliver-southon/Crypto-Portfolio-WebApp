from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from traders.forms import RegisterTraderForm

def login_trader(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("success")
            return redirect('holdings')
        else:
            print('failed')
            messages.success(request, "There was an error loggin in. Please try again.")
            return redirect('login')

    else:
        return render(request, 'authenticate/login.html', {})

def logout_trader(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('user-portfolio')

def register_trader(request):
    if request.method == "POST":
        form = RegisterTraderForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration successful!"))
            return redirect("holdings")
    else:
        form = RegisterTraderForm()

    return render(request, 'authenticate/register_trader.html', {
        'form':form
    })