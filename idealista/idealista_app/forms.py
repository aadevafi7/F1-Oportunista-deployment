
from django import forms

from .dummies import add_user, user_exists


class LoginForm(forms.Form):
    username = forms.EmailField(label='Email de acceso')
    password = forms.CharField(
        widget=forms.PasswordInput, label='Tu contraseña')
    remember = forms.BooleanField(label='Recordar tus datos')


class RegisterForm(forms.Form):
    email = forms.EmailField(label='Email de acceso')
    name = forms.CharField(label='Nombre')
    password = forms.CharField(
        widget=forms.PasswordInput, label='Tu contraseña')
    aceptar_privacidad = forms.BooleanField(
        label='Aceptar la política de privacidad')
    recibir_info = forms.BooleanField(label="""
        Recibir información de inmuebles,
        noticias y otras comunicaciones
        promocionales desde idealista,
        idealista/data, idealista/hipotecas o
        Rentalia basadas en tu perfil.""")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean_email_address(self):
        email = self.cleaned_data.get('email_address')
        if self.user and self.user.email == email:
            return email
        if user_exists(email):
            raise forms.ValidationError(u'That email address already exists.')
        return email
