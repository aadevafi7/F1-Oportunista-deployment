from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# Create your views here.

def register_user(request):
    
    return render(request, 'idealista_app/register.html')