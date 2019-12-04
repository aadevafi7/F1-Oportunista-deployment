from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import PropertyType, State, Province, Location, Property, PropertyPics

from .forms import LoginForm, RegisterForm, ChangePasswordForm

#from slugify import slugify

from .dummies import add_user, users
# Create your views here.


def placeholder(request):
    return render(request, 'idealista_app/placeholder.html')


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
    if request.method == 'GET':
        type_properties = PropertyType.objects.filter(id__gt=0)
        states = State.objects.filter(id__gt=0)
        context = {
            'type_properties': type_properties,
            'states': states,
        }
        return render(request, 'idealista_app/home.html', context)
    else:
        return render(request, 'idealista_app/home.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def submit(request):
    return render(request, 'idealista_app/submit.html')


def publicarAnuncio(request):
    return render(request, 'idealista_app/publicar-anuncio.html')


def publicarAnuncio2(request):
    return render(request, 'idealista_app/publicar-anuncio2.html')


def publicarAnuncio3(request):
    return render(request, 'idealista_app/publicar-anuncio3.html')


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


@login_required
def profile(request):
    return render(request, 'idealista_app/profile/profile.html')


@login_required
def myposts(request):
    if request.method == 'GET':
        user = request.user.id
        '''print(user)
        print(Property.objects.filter(user=user).values('city__name').select_related)'''
        properties_user = Property.objects.filter(user=user)
        context = {
            'properties_user': properties_user,
        }
        return render(request, 'idealista_app/profile/tus-anuncios.html', context)
    else:
        return render(request, 'idealista_app/profile/profile.html')


def posts(request, type="", state="", province="", location=""):
    if request.method == 'GET':
        if state:
            ads = ""
            locations = ""
            level = ""
            path = state
            if province:
                path += '/'+province
                if location:
                    ads = Property.objects.filter(pro_type__acr=type, city__acr=location)
                    level = Location.objects.get(acr=location)
                    path += '/'+location
                else:
                    ads = Property.objects.filter(pro_type__acr=type, city__province__acr=province)
                    locations = Location.objects.filter(province__acr=province)
                    level = Province.objects.get(acr=province)
            else:
                ads = Property.objects.filter(pro_type__acr=type, city__province__state__acr=state)
                locations = Province.objects.filter(state__acr=state)
                level = State.objects.get(acr=state)
        else:
            ads = Property.objects.all()
            locations = State.objects.all()
        context = {
            'posts': ads,
            'locations': locations,
            'level': level,
            'path': path,
        }
        return render(request, 'idealista_app/buscar-publicaciones.html', context)
    else:
        homePage(request)


#l=[]
# propietat= objects.filter(propietat)
#for p in propietat:
    # foto = objects.filter(propierty=p)
    #t (p, foto)
    #l.append(t)
#context =
