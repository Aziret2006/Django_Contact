from django.contrib import admin
from .models import Contact, PhoneNumber 

# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_active']
    list_filter = ['is_active', 'updated_date']
    search_fields = ['name', 'user__username']


class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ['contact', 'number', 'is_active']
    list_filter = ['is_active', 'updated_date']
    search_fields = ['number', 'contact__name']
    

admin.site.register(Contact, ContactAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
