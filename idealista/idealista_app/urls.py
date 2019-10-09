from django.conf.urls import url
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
        regex=r'^publish-add/',
        view=views.publish_add,
        name='publishAdd'
    )
]
