from django.db import models


class Contact(models.Model):
    email = models.EmailField(verbose_name='email', unique=True)
    phone = models.CharField(max_length=20, verbose_name='номер телефона', unique=True)
    country = models.CharField(max_length=100, verbose_name='страна')
    city = models.CharField(max_length=100, verbose_name='город')
    street = models.CharField(max_length=100, verbose_name='улица')
    number_home = models.IntegerField(verbose_name='номер дома')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
