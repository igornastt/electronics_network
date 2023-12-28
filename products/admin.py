from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_model', 'launch_date', 'is_active')
    list_filter = ('product_model', 'launch_date', 'is_active',)
    search_fields = ('name',)
