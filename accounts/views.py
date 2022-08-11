from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RegisterForm


# Create your views here.
def login_user(request):
    if request.method == "POST":
        print('POST')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'you are logged successed')
            # redirect_url = request.GET.get('next', 'home')
            return redirect('articles:pagination-list')
        else:
            messages.error(request, 'Bad username or password')
    
    print('GET')
    return render(request, 'accounts/login.html', {})

def logout_user(request):
    logout(request)
    return redirect('/')

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password1)
            login(request, user)
            return redirect("articles:pagination-list")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form":form})