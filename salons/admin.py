from django.contrib import admin
from .models import Salon, Service, Employee, EmployeeWorkingHours, EmployeeDaysOff, SalonCustomer

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


@admin.register(EmployeeWorkingHours)
class EmployeeWorkingHoursAdmin(admin.ModelAdmin):
    list_display = ('employee', 'day', 'start_time', 'end_time', 'is_day_off')

@admin.register(EmployeeDaysOff)
class EmployeeDaysOffAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'reason','days_count')

    def days_count(self, obj):
        return (obj.end_date - obj.start_date).days + 1

@admin.register(SalonCustomer)
class SalonCustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'salon', 'is_active', 'phone_number', 'full_name', 'address', 'email', 'birth_date', 'gender')
