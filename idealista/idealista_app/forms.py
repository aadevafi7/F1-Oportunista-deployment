
from django import forms
from django.contrib.auth.models import User

from .dummies import add_user, user_exists


class LoginForm(forms.Form):
    username = forms.EmailField(label='Email de acceso')
    password = forms.CharField(
        widget=forms.PasswordInput, label='Tu contraseña')
    remember = forms.BooleanField(label='Recordar tus datos', required=False)


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
        Rentalia basadas en tu perfil.""", required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RegisterForm, self).__init__(*args, **kwargs)

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)
        self.validate_email(value.email)

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email
        raise forms.ValidationError('Este email ya está registrado.')

    def save(self, commit=True):
        name = self.cleaned_data.get('name')

        # using email as username
        email = self.cleaned_data.get('email')
        raw_password = self.cleaned_data.get('password')
        recibir_info = self.cleaned_data.get('recibir_info')

        user = User.objects.create_user(
            email, email, raw_password
        )
        user.save()
