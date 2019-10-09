
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
        print(f'Validating {email}.')

        if user_exists(email):
            print(f'Email already exists.')
            raise forms.ValidationError('Este email ya está registrado.')
        return email
