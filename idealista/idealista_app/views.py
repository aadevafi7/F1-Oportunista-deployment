from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth

from .forms import LoginForm, RegisterForm

from .dummies import add_user, users
# Create your views here.


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = auth.authenticate(
                username=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password'))
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect('idealista_app:homePage')
            else:
                return HttpResponse('Unauthorized', status=401)
    else:
        form = RegisterForm()
    return render(request, 'idealista_app/register.html', {'form': form})


def homePage(request):
    if request.user.is_authenticated:
        pass
    else:
        pass
    return render(request, 'idealista_app/home.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def submit(request):
    return render(request, 'idealista_app/submit.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'))
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect('idealista_app:homePage')
            else:
                return HttpResponse('Unauthorized', status=401)
    else:
        form = LoginForm()
    return render(request, 'idealista_app/login.html', {'form': form})


def profile(request):
    if request.user.is_authenticated:
        profile = request.user.userprofile
        return render(request, 'idealista_app/profile/profile.html', {'profile': profile})
    else:
        return HttpResponse('Unauthorized', status=401)
