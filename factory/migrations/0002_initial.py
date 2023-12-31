# Generated by Django 5.0 on 2023-12-28 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('factory', '0001_initial'),
        ('networks_electronics', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='factory',
            name='main_network',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_network_factory', to='networks_electronics.mainnetwork', verbose_name='основная сеть'),
        ),
        migrations.AddField(
            model_name='factory',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='factory_products', to='products.product'),
        ),
    ]
