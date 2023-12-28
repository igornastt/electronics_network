from django.contrib import admin

from networks_electronics.models.main_network_models import MainNetwork
from contacts.services import ContactCityFilter


@admin.register(MainNetwork)
class MainNetworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact', 'created_at', 'is_active',)
    list_filter = ('name', ContactCityFilter, 'is_active',)
    search_fields = ('name',)
