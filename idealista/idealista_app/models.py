from django.db import models
from django.contrib.auth.models import User

'''
----------------------------------------------
Modelos / tablas de la aplicación Oportunista
----------------------------------------------
'''


class PropertyType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Province(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    
     def __str__(self):
        return self.name


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    
     def __str__(self):
        return self.name


class Property(models.Model):
    id = models.AutoField(primary_key=True)
    pro_type = models.ForeignKey(PropertyType, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    op_type = models.IntegerField(blank=True, null=True)
    description = models.TextField(max_length=500)
    address = models.CharField(max_length=150)
    address_number = models.CharField(max_length=5, blank=True, null=True)
    floor = models.CharField(max_length=15, blank=True, null=True)
    door = models.CharField(max_length=15, blank=True, null=True)
    m_built = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    m_use = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    rooms = models.IntegerField(blank=True, null=True)
    bath = models.IntegerField(blank=True, null=True)
    is_exterior = models.SmallIntegerField(blank=True, null=True)
    has_elevator = models.SmallIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    city = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=9)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' (' + self.city + ')'


class PropertyPics(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.ImageField
    order = models.IntegerField
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
