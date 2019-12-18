from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import OperationType, PropertyType, State, Province, Location, Property, PropertyPics

from .forms import LoginForm, RegisterForm, ChangePasswordForm, PropertyForm

# from slugify import slugify

from .dummies import add_user, users


# Create your views here.


def placeholder(request, id=""):
    if request.method == 'GET':
        property = Property.objects.get(
                    id__icontains=id)
        context = {
            'property': property,
        }
        return render(request, 'idealista_app/placeholder.html', context)
    else:
        homePage(request)


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
                return HttpResponseRedirect('idealista_app:register_user')
    else:
        form = RegisterForm()
    return render(request, 'idealista_app/register.html', {'form': form})


def get_posts(request, operation, type, state):
    if state:
        state = State.objects.get(name=state)
        type = PropertyType.objects.get(name=type)
        operation = OperationType.objects.get(name=operation)
        # t = PropertyType.objects.filter(name=type).first()
        ads = Property.objects.filter(
            op_type=operation, pro_type=type, city__province__state=state)
        locations = Province.objects.filter(state=state)
        path = '/'.join([operation.acr, type.acr, state.acr])

        context = {
            'posts': ads,
            'locations': locations,
            'level': state,
            'path': path,
        }
        return render(request, 'idealista_app/buscar-publicaciones.html', context)


def homePage(request):

    if request.method == 'GET':
        type_operation = OperationType.objects.filter(id__gt=0)
        type_properties = PropertyType.objects.filter(id__gt=0)
        states = State.objects.filter(id__gt=0)
        context = {
            'type_operations': type_operation,
            'type_properties': type_properties,
            'states': states,
        }
        return render(request, 'idealista_app/home.html', context)
    elif request.method == 'POST':
        return get_posts(request, operation=request.POST['op'], type=request.POST['tipo'], state=request.POST['comunidad'])


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def submit(request):
    return render(request, 'idealista_app/submit.html')


@login_required
def publicarAnuncio(request):

    """
    # Cloudinary -------------------------------------------------------------------------------------------------------
    unsigned = request.GET.get("unsigned") == "true"
    if (unsigned):
        try:
            api.upload_preset(PhotoUnsignedDirectForm.upload_preset_name)
        except api.NotFound:
            api.create_upload_preset(name=PhotoUnsignedDirectForm.upload_preset_name, unsigned=True,
                                     folder="preset_folder")

    direct_form = PhotoUnsignedDirectForm() if unsigned else PhotoDirectForm()
    context = dict(
        # Form demonstrating backend upload
        backend_form=PropertyForm(),
        # Form demonstrating direct upload
        direct_form=direct_form,
        # Should the upload form be unsigned
        unsigned=unsigned,
    )
    # When using direct upload - the following call is necessary to update the
    # form's callback url
    cl_init_js_callbacks(context['direct_form'], request)

     Cloudinary END ---------------------------------------------------------------------------------------------------
    """

    if request.method == 'POST':
        form = PropertyForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('idealista_app:homePage')
        else:
            pass  # print(form.errors)
    else:
        form = PropertyForm(request.user)
    return render(request, 'idealista_app/publicar-anuncio.html', {'form': form})


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
                return HttpResponseRedirect('idealista_app:login')
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
    elif request.method == 'POST':
        Property.objects.get(id=request.POST['deletePost']).delete()
        user = request.user.id
        properties_user = Property.objects.filter(user=user)
        context = {
            'properties_user': properties_user,
        }
        return render(request, 'idealista_app/profile/tus-anuncios.html', context)
    else:
        return render(request, 'idealista_app/profile/profile.html')


def buscar_post(request):
    print('aaa')
    return render(request, 'idealista_app/profile/profile.html')


def posts(request, operation="", type="", state="", province="", location=""):
    if request.method == 'GET':
        if state:
            ads = ""
            locations = ""
            level = ""
            path = operation + '/' + type + '/' + state
            if province:
                path += '/'+province
                if location:
                    ads = Property.objects.filter(
                        op_type__acr=operation, pro_type__acr=type, city__acr=location)
                    level = Location.objects.get(acr=location)
                    path += '/'+location
                else:
                    ads = Property.objects.filter(
                        op_type__acr=operation, pro_type__acr=type, city__province__acr=province)
                    locations = Location.objects.filter(province__acr=province)
                    level = Province.objects.get(acr=province)
            else:
                ads = Property.objects.filter(
                    op_type__acr=operation, pro_type__acr=type, city__province__state__acr=state)
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

def quienessomos(request):
      return render(request,'idealista_app/quienesSomos.html')


# l=[]
# propietat= objects.filter(propietat)
# for p in propietat:
    # foto = objects.filter(propierty=p)
    # t (p, foto)
    # l.append(t)
# context =
