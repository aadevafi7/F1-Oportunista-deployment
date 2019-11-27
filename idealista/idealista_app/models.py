from django.db import models
from django.contrib.auth.models import User

'''
----------------------------------------------
Modelos / tablas de la aplicación Oportunista
----------------------------------------------
'''


class property_type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class state(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

class province(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    comunitat = models.ForeignKey(state, on_delete=models.DO_NOTHING)

class location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    provincia = models.ForeignKey(province, on_delete=models.DO_NOTHING)


class property(models.Model):
    id = models.AutoField(primary_key=True)
    pro_type = models.ForeignKey(property_type, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    op_type = models.IntegerField
    description = models.TextField(max_length=500)
    address = models.CharField(max_length=150)
    address_number = models.CharField(max_length=5)
    floor = models.CharField(max_length=15)
    door = models.CharField(max_length=15)
    m_built = models.DecimalField(max_digits=15, decimal_places=2)
    m_use = models.DecimalField(max_digits=15, decimal_places=2)
    rooms = models.IntegerField()
    bath = models.IntegerField()
    is_exterior = models.SmallIntegerField()
    has_elevator = models.SmallIntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    city = models.ForeignKey(location, on_delete=models.DO_NOTHING)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=9)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' (' + self.city + ')'


class property_pics(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.ImageField
    order = models.IntegerField
    property = models.ForeignKey(property, on_delete=models.CASCADE)
