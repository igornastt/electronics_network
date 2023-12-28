from django.db import models

from products.models import Product
from contacts.models import Contact


class MainNetwork(models.Model):
    name = models.CharField(max_length=100, verbose_name='имя', unique=True)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name='main_network_contact')
    products = models.ManyToManyField(Product, related_name='main_network_product', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Основная сеть'
        verbose_name_plural = 'Основные сети'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.contact.is_active = False
        self.contact.save()
        self.save()
