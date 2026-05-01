# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator, MaxLengthValidator

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    bio = models.CharField(
        max_length=100,
        blank=True,
        validators=[MaxLengthValidator(100)]
    )

    blocked_channels = models.ManyToManyField(
        'chat.Channel',
        related_name='blocked_by_users',
        blank=True
    )

    def __str__(self):
        return self.username