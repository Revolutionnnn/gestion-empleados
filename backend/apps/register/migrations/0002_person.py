# Generated by Django 5.0.6 on 2024-08-21 16:57

import django.db.models.deletion
import django_extensions.db.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('name', models.CharField(max_length=30, verbose_name='Nombre')),
                ('type', models.PositiveBigIntegerField(choices=[(1, 'Empleado'), (2, 'Invitado'), (3, 'Proveedor')], verbose_name='Tipo de persona')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Teléfono')),
                ('document', models.CharField(max_length=50, unique=True, verbose_name='Documento')),
                ('rol', models.CharField(blank=True, max_length=50, null=True, verbose_name='Rol')),
                ('bussines', models.CharField(blank=True, max_length=100, null=True, verbose_name='Empresa')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_area', to='register.area', verbose_name='Área')),
            ],
            options={
                'verbose_name': 'Persona',
                'verbose_name_plural': 'Personas',
            },
        ),
    ]
