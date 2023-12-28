from django.db import models
from rest_framework.exceptions import ValidationError

from products.models import Product
from contacts.models import Contact
from factory.models import Factory
from networks_electronics.models.main_network_models import MainNetwork
from networks_electronics.models.retail_network_models import RetailNetwork


NULLABLE = {'blank': True, 'null': True}


class SoleProprietor(models.Model):
    main_network = models.ForeignKey(
        MainNetwork, verbose_name='основная сеть', related_name='main_network_proprietor', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True, verbose_name='имя индивидуального предпринимателя')
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name='proprietor_contacts')
    products = models.ManyToManyField(Product, related_name='proprietor_products', blank=True)
    factory_supplier = models.ForeignKey(Factory, on_delete=models.SET_NULL,
                                         verbose_name='завод-поставщик',
                                         related_name='factory_supplier_for_proprietor', **NULLABLE)
    retail_network_supplier = models.ForeignKey(RetailNetwork, on_delete=models.SET_NULL,
                                                verbose_name='поставщик розничная сеть',
                                                related_name='retail_network_supplier', **NULLABLE)
    debt_to_supplier = models.DecimalField(verbose_name='задолженность перед поставщиком', decimal_places=2,
                                           max_digits=25, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'"{self.name}" предприниматель'

    class Meta:
        verbose_name = 'Индивидуальный предприниматель'
        verbose_name_plural = 'Индивидуальные предприниматели'

    def clean(self):
        if self.factory_supplier and self.retail_network_supplier:
            message = "Индивидуальный предприниматель может иметь только одного поставщика (либо factory_supplier, либо retail_network_supplier)."
            raise ValidationError(message)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.contact.is_active = False
        self.contact.save()
        self.save()
