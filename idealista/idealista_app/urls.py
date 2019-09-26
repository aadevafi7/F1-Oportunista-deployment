from django.conf.urls import url
from . import views
from idealista_app.views import register_user

urlpatterns =[

    url(
        regex=r'^register/$',
        view=views.register_user,
        name='register_user'
    )
]
