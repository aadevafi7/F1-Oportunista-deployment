# Generated by Django 2.2.5 on 2019-10-13 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='property',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500)),
                ('address', models.CharField(max_length=150)),
                ('floor', models.CharField(max_length=15)),
                ('door', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=9)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='idealista_app.location')),
            ],
        ),
        migrations.CreateModel(
            name='property_type',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='property_pics',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='idealista_app.property')),
            ],
        ),
        migrations.AddField(
            model_name='property',
            name='pro_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='idealista_app.property_type'),
        ),
        migrations.AddField(
            model_name='property',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
