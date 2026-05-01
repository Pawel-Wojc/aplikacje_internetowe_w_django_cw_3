from django.conf import settings
from django.db import models

#tutaj damy logike ze jak typ prywatny, to to beda DM, a odbiorca nadawca to members
class Channel(models.Model):
    CHANNEL_TYPES = [
        ('public', 'Publiczny'),
        ('private', 'Prywatny'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    channel_type = models.CharField(max_length=20, choices=CHANNEL_TYPES, default='public')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_channels'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='joined_channels',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Message(models.Model):
    MESSAGE_TYPES = [
        ('text', 'Tekst'),
        ('image', 'Obraz'),
        ('audio', 'Audio'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name='messages',
        null=True,
        blank=True
    )
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author} -> {self.channel}: {self.content[:30]}'

    content = models.TextField(blank=True)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='text')
    image = models.ImageField(upload_to='messages/images/', blank=True, null=True)
    audio = models.FileField(upload_to='messages/audio/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
