from django.contrib.auth.models import AbstractUser
from django.db import models

from users.manager import UserManager

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Класс для отображения пользователей"""

    username = None

    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=30, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=235, verbose_name='страна')
    city = models.CharField(max_length=235, verbose_name='город')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email
