
from django import forms
from django.contrib.auth.models import User

from .dummies import add_user, user_exists


class LoginForm(forms.Form):
    username = forms.EmailField(label='Email de acceso')
    password = forms.CharField(
        widget=forms.PasswordInput, label='Tu contraseña')
    remember = forms.BooleanField(label='Recordar tus datos', required=False)


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput, label='Contraseña actual')
    new_password = forms.CharField(
        widget=forms.PasswordInput, label='Nueva contraseña', help_text="Utiliza al menos 4 caracteres, letras y números")
    repeat_password = forms.CharField(
        widget=forms.PasswordInput, label='Vuelve a escribir la nueva contraseña')
    remember = forms.BooleanField(
        label="Recuérdame en este dispositivo", required=False)

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)
        np = self.cleaned_data.get('new_password')
        rp = self.cleaned_data.get('repeat_password')
        if np != rp:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        self.validate_email(value.email)


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

        # using email as username
        email = self.cleaned_data.get('email')
        name = self.cleaned_data.get('name')
        raw_password = self.cleaned_data.get('password')
        recibir_info = self.cleaned_data.get('recibir_info')

        user = User.objects.create_user(
            email, email, raw_password, first_name=name
        )
        user.save()
