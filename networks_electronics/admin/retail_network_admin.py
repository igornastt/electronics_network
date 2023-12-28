from django.contrib import admin

from contacts.services import ContactCityFilter
from networks_electronics.models.retail_network_models import RetailNetwork
from sole_proprietor.admin import clear_debt


@admin.register(RetailNetwork)
class RetailNetworkAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'main_network', 'factory_supplier', 'debt_to_supplier', 'contact', 'created_at', 'is_active'
    )
    list_filter = ('factory_supplier', ContactCityFilter, 'is_active',)
    search_fields = ('name',)
    actions = [clear_debt]
