from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
import uuid


class CustomUser(AbstractUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(max_length=150, unique=True)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        if not self.pk and not self.is_superuser:
            if not self.password:
                random_password = get_random_string(length=8)
                self.set_password(random_password)
                send_mail(
                    'Tu contraseña de usuario',
                    f'Tu contraseña temporal es: {random_password} del usuario {self.username}',
                    'from@example.com',  # Cambia esto a tu dirección de correo
                    [self.email],
                    fail_silently=False,
                )
        super().save(*args, **kwargs)
