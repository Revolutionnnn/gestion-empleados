from django_extensions.db.models import TimeStampedModel
from django.db import models
import uuid


class Area(TimeStampedModel):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="UUID"
    )
    name = models.CharField(
        max_length=30,
        verbose_name="Nombre"
    )
    description = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Descripción"
    )


class Person(TimeStampedModel):
    EMPLEYEE = 1
    GUEST = 2
    PROVIDER = 3

    TYPE_CHOICES = [
        (EMPLEYEE, 'Empleado'),
        (GUEST, 'Invitado'),
        (PROVIDER, 'Proveedor')
    ]
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="UUID"
    )
    name = models.CharField(
        max_length=30,
        verbose_name="Nombre"
    )
    type = models.PositiveBigIntegerField(
        choices=TYPE_CHOICES,
        verbose_name="Tipo de persona"
    )
    phone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Teléfono"
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        related_name='person_area',
        verbose_name="Área"
    )
    document = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Documento"
    )
    rol = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Rol"
    )
    bussines = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Empresa"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
