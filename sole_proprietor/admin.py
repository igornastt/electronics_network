from django.contrib import admin
from sole_proprietor.models import SoleProprietor
from contacts.services import ContactCityFilter


@admin.action(description="Assigns debt_to_supplier with 0.00.")
def clear_debt(model_admin, request, queryset):
    queryset.update(debt_to_supplier=0)


@admin.register(SoleProprietor)
class SoleProprietorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'main_network', 'factory_supplier', 'retail_network_supplier', 'contact',
                    'debt_to_supplier', 'created_at', 'is_active',)
    list_filter = ('factory_supplier', 'retail_network_supplier', ContactCityFilter, 'is_active',)
    search_fields = ('name',)
    actions = [clear_debt]
