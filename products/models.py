from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='название продукта', unique=True)
    product_model = models.CharField(max_length=50, verbose_name='модель продукта')
    launch_date = models.DateField(verbose_name='дата выхода продукта на рынок')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
