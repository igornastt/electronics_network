from django.contrib import admin

from contacts.models import Contact


class ContactCityFilter(admin.SimpleListFilter):
    """
    Класс фильтр для админ-панели по полю City из модели Contact.
    """
    title = 'City'
    parameter_name = 'contact_city'

    def lookups(self, request, model_admin):
        cities = Contact.objects.values_list('city', flat=True).distinct()
        return [(city, city) for city in cities]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(contact_city=self.value())
        return queryset
