from django.db import models

from products.models import Product
from networks_electronics.models.main_network_models import MainNetwork
from contacts.models import Contact


class Factory(models.Model):
    main_network = models.ForeignKey(
        MainNetwork, verbose_name='основная сеть', related_name='main_network_factory', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True, verbose_name='название завода')
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name='factory_contacts')
    products = models.ManyToManyField(Product, related_name='factory_products', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'завод "{self.name}"'

    class Meta:
        verbose_name = 'Завод'
        verbose_name_plural = 'Заводы'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.contact.is_active = False
        self.contact.save()
        self.save()