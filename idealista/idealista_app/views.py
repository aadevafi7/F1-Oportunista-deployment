from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from .forms import LoginForm, RegisterForm, PublishAddForm

from .dummies import add_user, users
# Create your views here.


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('idealista_app:homePage')
    else:
        form = RegisterForm()
    return render(request, 'idealista_app/register.html', {'form': form})


def homePage(request):
    print(users)
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


def publish_add(request):
    if request.method == 'POST':
        form = PublishAddForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('idealista_app:homePage')
    else:
        form = PublishAddForm()
    return render(request, 'idealista_app/publish-add.html', {'form': form})