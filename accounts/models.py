from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # nie ma tu username bo jest dziedziczony z AbstractUser, ale dodajemy email, avatar i bio
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)


    #tutaj uzytkownik ma properties dzieki kroremy bedzie wiadomo do ktorych kanalow zostal zablokowany
    blocked_channels = models.ManyToManyField('chat.Channel', related_name='blocked_by_users', blank=True)

    def __str__(self):
        return self.username