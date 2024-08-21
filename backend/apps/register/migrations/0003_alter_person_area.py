# Generated by Django 5.0.6 on 2024-08-21 18:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person_area', to='register.area', verbose_name='Área'),
        ),
    ]
