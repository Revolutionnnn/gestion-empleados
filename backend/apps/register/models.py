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
