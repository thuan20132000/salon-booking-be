from django.contrib import admin

# Register your models here.
from .models import Booking, BookingService, Review, BookingPayment

class BookingServiceInline(admin.TabularInline):
    model = BookingService
    extra = 1

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer', 
        'salon', 
        'status', 
        'created_at',
    )
    inlines = [BookingServiceInline]
@admin.register(BookingService)
class BookingServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'service', 'employee', 'status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'rating', 'created_at')


@admin.register(BookingPayment)
class BookingPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'payment_method', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


