from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .forms import LoginForm
# Create your views here.


def register_user(request):
    return render(request, 'idealista_app/register.html')

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
        return render(request, 'idealista_app/login.html', { 'form': form })
