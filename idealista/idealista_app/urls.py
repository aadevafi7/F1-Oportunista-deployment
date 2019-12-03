from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(
        regex=r'^register/$',
        view=views.register_user,
        name='register_user'
    ),
    url(
        regex=r'^home/$',
        view=views.homePage,
        name='homePage'
    ),
    url(
        regex=r'^submit/$',
        view=views.submit,
        name='submit'
    ),
    url(
        regex=r'^login/',
        view=views.login,
        name='login'
    ),
    url(
        regex=r'^logout/',
        view=views.logout,
        name='logout'
    ),
    url(
        regex=r'^placeholder/',
        view=views.placeholder,
        name='placeholder'
    ),
    url(
        regex=r'^publicar-anuncio/',
        view=views.publicarAnuncio,
        name='publicarAnuncio'
    ),
    url(
        regex=r'^publicar-anuncio2/',
        view=views.publicarAnuncio2,
        name='publicarAnuncio2'
    ),
    url(
        regex=r'^publicar-anuncio3/',
        view=views.publicarAnuncio3,
        name='publicarAnuncio3'
    ),
    url(
        regex=r'^profile/',
        view=views.profile,
        name='profile'
    ),
    path(r'posts/<slug:type>/<state>/', views.posts, name='posts'),
    path(r'posts/<slug:type>/<state>/<province>/', views.posts, name='posts'),
    path(r'posts/<slug:type>/<state>/<province>/<location>/', views.posts, name='posts'),
]
