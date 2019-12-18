from django import forms
from django.contrib.auth.models import User

from .dummies import add_user, user_exists
from .models import *
from cloudinary.forms import CloudinaryJsFileField, CloudinaryUnsignedJsFileField
from cloudinary.compat import to_bytes
import cloudinary, hashlib


class LoginForm(forms.Form):
    username = forms.EmailField(label='Email de acceso')
    password = forms.CharField(
        widget=forms.PasswordInput, label='Tu contraseña')
    remember = forms.BooleanField(label='Recordar tus datos', required=False)


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput, label='Contraseña actual')
    new_password = forms.CharField(
        widget=forms.PasswordInput, label='Nueva contraseña',
        help_text="Utiliza al menos 4 caracteres, letras y números")
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


class PropertyForm(forms.Form):
    # property type

    pro_type = forms.ChoiceField(
        label='Tipo de inmueble', choices=[])

    name = forms.CharField(label='Nombre*')

    op_type = forms.ChoiceField(
        label='Operación', choices=[])
    description = forms.CharField(label="Descripción*", widget=forms.Textarea)
    address = forms.CharField(label="Dirección*")
    address_number = forms.CharField(label='Número*', max_length=5)

    floor = forms.CharField(label='Piso', max_length=15, required=False)
    door = forms.CharField(label='Puerta', max_length=15, required=False)
    m_built = forms.DecimalField(
        label='Metros construidos*', max_digits=15, decimal_places=2)
    m_use = forms.DecimalField(
        label='Metros útiles*', max_digits=15, decimal_places=2)

    bath = forms.IntegerField(label='Numero de baños*')
    rooms = forms.IntegerField(label='Numero de habitaciones*')
    is_exterior = forms.BooleanField(label='Es exterior?', required=False)
    has_elevator = forms.BooleanField(label='Tiene ascensor?', required=False)
    price = forms.DecimalField(label='Precio*')

    state = forms.ChoiceField(label='Comunidad*', choices=[])
    province = forms.ChoiceField(label='Provincia*', choices=[])
    city = forms.ChoiceField(label='Ciudad*', choices=[])

    phone = forms.IntegerField(
        label='Número de teléfono*', max_value=999999999, min_value=600000000)

    photo = forms.ImageField(label="Foto del inmueble", required=False)

    # user

    def __init__(self, user, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['op_type'].choices = [
            (p, p.name) for p in OperationType.objects.all()]
        self.fields['pro_type'].choices = [
            (p, p.name) for p in PropertyType.objects.all()]
        self.fields['state'].choices = [(c, c.name)
                                        for c in State.objects.all()]
        self.fields['province'].choices = [(':'.join([c.state.name, c.name]), c.name)
                                           for c in Province.objects.all()]
        self.fields['city'].choices = [(':'.join([c.province.name, c.name]), c.name)
                                       for c in Location.objects.all()]

    def clean_city(self):
        email = self.cleaned_data['city']

        try:
            return email.split(':')[1]
        except IndexError:
            # Unable to find a user, this is fine
            raise forms.ValidationError('Este email ya está registrado.')

    def save(self, commit=True):
        op_type_value = self.cleaned_data.get("op_type")
        op_type = OperationType.objects.filter(name=op_type_value).first()
        pro_type_value = self.cleaned_data.get("pro_type")
        pro_type = PropertyType.objects.filter(name=pro_type_value).first()
        # state_value = self.cleaned_data.get("state")
        # state = State.objects.filter(name=state_value).first()
        # province_value = self.cleaned_data.get("province")
        # province = Province.objects.filter(name=province_value).first()
        city_value = self.cleaned_data.get("city")
        city = Location.objects.filter(name=city_value).first()
        out = self.cleaned_data.copy()
        out['op_type'] = op_type
        out['pro_type'] = pro_type
        del out['state']
        del out['province']
        # del out['photo']  # TODO
        out['city'] = city
        out['user'] = self.user
        p = Property.objects.create(**out)
        p.save()