from django.contrib import admin
from .models import Salon, Service, Employee

# Register your models here.

class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 1

@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email')
    inlines = [EmployeeInline]
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'salon', 'role', 'is_active', 'is_available')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'salon', 'price', 'duration')