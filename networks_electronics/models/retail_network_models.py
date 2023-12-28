from django.db import models

from factory.models import Factory
from products.models import Product
from contacts.models import Contact
from networks_electronics.models.main_network_models import MainNetwork

NULLABLE = {'blank': True, 'null': True}


class RetailNetwork(models.Model):
    main_network = models.ForeignKey(
        MainNetwork, verbose_name='основная сеть', related_name='main_network_retail_net', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True, verbose_name='название сети')
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name='network_contacts')
    products = models.ManyToManyField(Product, related_name='network_products', blank=True)
    factory_supplier = models.ForeignKey(Factory, on_delete=models.SET_NULL,
                                         verbose_name='поставщик', related_name='supplier', **NULLABLE)
    debt_to_supplier = models.DecimalField(verbose_name='debt_to_supplier', decimal_places=2, max_digits=15, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'"{self.name}" сеть'

    class Meta:
        verbose_name = 'Розничная сеть'
        verbose_name_plural = 'Розничные сети'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.contact.is_active = False
        self.contact.save()
        self.save()
