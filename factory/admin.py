from django.contrib import admin

from factory.models import Factory
from contacts.services import ContactCityFilter


@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'main_network', 'contact', 'created_at', 'is_active',)
    list_filter = ('name', ContactCityFilter, 'is_active',)
    search_fields = ('name',)
