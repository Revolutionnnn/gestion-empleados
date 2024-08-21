from apps.register.models import Person
from django_extensions.db.models import TimeStampedModel
from django.db import models
import uuid


class Check(TimeStampedModel):
    MEDICAL_QUOTE = 1
    CALAMITY = 2
    PERSONAL_DILIGENCE = 3

    REASON_CHOICES = [
        (MEDICAL_QUOTE, 'Cita médica'),
        (CALAMITY, 'Calamidad'),
        (PERSONAL_DILIGENCE, 'Diligencia personal')
    ]

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="UUID"
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name="Persona"
    )
    check_in = models.DateTimeField(
        verbose_name="Hora de entrada"
    )
    check_out = models.DateTimeField(
        verbose_name="Hora de salida",
        blank=True,
        null=True
    )
    reason = models.PositiveIntegerField(
        choices=REASON_CHOICES,
        verbose_name="Motivo",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Registro"
        verbose_name_plural = "Registros"
