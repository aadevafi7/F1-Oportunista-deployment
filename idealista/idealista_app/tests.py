from django.test import TestCase

from decimal import Decimal
from django.contrib.auth.models import User
from .models import PropertyType, Property, Location, State, Province, Location
from .forms import LoginForm, RegisterForm
# Create your tests here.


class LoginTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'test@user.com',
            'password': '1234abcd'
        }
        User.objects.create_user(**self.credentials)

    def test_validForm(self):
        form = LoginForm(data=self.credentials)
        self.assertTrue(form.is_valid())

    def test_login(self):
        response = self.client.post(
            '/login/',
            self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)


class LogoutTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'test@user.com',
            'password': '1234abcd'
        }
        User.objects.create_user(**self.credentials)

    def test_logout(self):
        response = self.client.post(
            '/logout/', follow=True)
        self.assertFalse(response.context['user'].is_authenticated)


class RegisterTest(TestCase):
    def setUp(self):
        self.credentials = {
            'email': 'test@testmail.com',
            'password': '1234abcd',
            'name': 'TestName',
            'aceptar_privacidad': 'on',
        }

    def test_validForm(self):
        form = RegisterForm(data=self.credentials)
        self.assertTrue(form.is_valid())

    def test_register(self):
        response = self.client.post(
            '/register/',
            self.credentials, follow=True)

        self.assertTrue(response.context['user'].is_active)
        try:
            user = User.objects.get(username=self.credentials['email'])
            self.assertEqual(user.username, self.credentials['email'])
            self.assertEqual(user.email, self.credentials['email'])
            self.assertEqual(user.first_name, self.credentials['name'])
            self.assertTrue(user.check_password(self.credentials['password']))

        except User.DoesNotExist:
            self.fail('Newly created user not found in database')


class MyPostsTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'test@user.com',
            'name': 'TestName',
            'password': '1234abcd'
        }
        User.objects.create_user(**self.credentials)
        PropertyType.objects.create(name='Comprar')
        ptype_id = PropertyType.objects.get(name='Comprar').values('id')
        user = User.objects.get(
            username=self.credentials['email']).values('id')
        Property.objects.create(pro_type=ptype_id, name='Piso test', description='Piso bonito con vistas a la UB',
                                address='Gran Via 476', floor='4', door='5', rooms=4, bath=2, price=200000, city=1,
                                email='test@email.com', phone='6789', user=user)

    def test_viewMyPosts(self):
        self.client.login(username='test@user.com', password='1234abcd')
        response = self.client.post(
            '/myposts/', follow=True)
        try:
            property = response.context['properties_user'][0]
            self.assertEqual(property.name, 'Piso test')
            self.assertEqual(property.rooms, 4)
        except User.DoesNotExist:
            self.fail('Newly created user not found in database')


class CreatePostTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'test@user.com',
            # 'name': 'TestName',
            'password': '1234abcd'
        }
        User.objects.create_user(**self.credentials)
        PropertyType.objects.create(name='Comprar')
        ptype = PropertyType.objects.get(name='Comprar')
        user = User.objects.get(
            username=self.credentials['username'])
        state = State.objects.create(name='Cataluña')
        prov = Province.objects.create(name='Tarragona', state=state)
        self.city = Location.objects.create(name='Salou', province=prov)
        self.object = dict(pro_type=ptype, op_type=1, name='Piso test', description='Piso bonito con vistas a la UB',
                           address='Gran Via 476', address_number='1', m_use=Decimal('100.00'), m_built=Decimal('100.00'), floor='4', door='5', rooms=4, bath=2, price=Decimal('200000'), city="Tarragona:Salou", state='Cataluña', province='Cataluña:Tarragona',
                           email='', phone='123456789', user=user)

    def test_createPost(self):
        self.client.login(username='test@user.com', password='1234abcd')
        response = self.client.post(
            '/publicar-anuncio/', self.object, follow=True)

        self.assertRaises(KeyError, lambda: response.context['form'])
        try:
            prop = Property.objects.all().first()
            for k, v in self.object.items():
                if k == 'city':
                    v = self.city
                if hasattr(prop, k):
                    self.assertEqual(v, getattr(prop, k))
        except Property.DoesNotExist:
            self.fail('Newly created property not found in database')
