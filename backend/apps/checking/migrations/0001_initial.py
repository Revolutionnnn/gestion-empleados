# Generated by Django 5.0.6 on 2024-08-21 21:38

import django.db.models.deletion
import django_extensions.db.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('register', '0004_rename_bussines_person_business'),
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('check_in', models.DateTimeField(verbose_name='Hora de entrada')),
                ('check_out', models.DateTimeField(blank=True, null=True, verbose_name='Hora de salida')),
                ('reason', models.PositiveIntegerField(blank=True, choices=[(1, 'Cita médica'), (2, 'Calamidad'), (3, 'Diligencia personal')], null=True, verbose_name='Motivo')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.person', verbose_name='Persona')),
            ],
            options={
                'verbose_name': 'Registro',
                'verbose_name_plural': 'Registros',
            },
        ),
    ]
