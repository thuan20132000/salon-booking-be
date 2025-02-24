from django.contrib import admin
from .models import Customer

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'address')
    search_fields = ('full_name', 'phone_number', 'address')
    list_filter = ('full_name', 'phone_number', 'address')

