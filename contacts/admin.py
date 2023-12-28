from django.contrib import admin

from contacts.models import Contact


class ContactInline(admin.StackedInline):
    model = Contact
    list_display = ('email', 'phone', 'country', 'city', 'street', 'number_home', 'is_active',)
    list_filter = ('country', 'city', 'is_active',)
    search_fields = ('email', 'phone',)


admin.site.register(Contact)
