from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from .forms import LoginForm, RegisterForm

from .dummies import add_user
# Create your views here.


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('name')
            email = form.clean_email_address()
            raw_password = form.cleaned_data.get('password')
            add_user(username, email, raw_password)
            return redirect('home')
    else:
        form = RegisterForm()
        return render(request, 'idealista_app/register.html', {'form': form})


def homePage(request):
    return render(request, 'idealista_app/home.html')


def submit(request):
    return render(request, 'idealista_app/submit.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()
        return render(request, 'idealista_app/login.html', {'form': form})
