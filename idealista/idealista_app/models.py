from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class oportunista_property_type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class oportunista_location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)


class oportunista_property(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=50)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name + ' (' + self.city + ')'

class oportunista_property_pics(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.ImageField
    property = models.ForeignKey(oportunista_property)
