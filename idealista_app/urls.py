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
        regex=r'^publicar-anuncio/',
        view=views.publicarAnuncio,
        name='publicarAnuncio'
    ),
    url(
        regex=r'^profile/',
        view=views.profile,
        name='profile'
    ),
    url(
        regex=r'^myposts',
        view=views.myposts,
        name='myposts'
    ),
    path(r'posts/<slug:operation>/<slug:type>/<state>/', views.posts, name='posts'),
    path(r'posts/<slug:operation>/<slug:type>/<state>/<province>/', views.posts, name='posts'),
    path(r'posts/<slug:operation>/<slug:type>/<state>/<province>/<location>/', views.posts, name='posts'),
    path(r'placeholder/<id>/', views.placeholder, name='placeholder'),
]
