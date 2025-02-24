from rest_framework import serializers
from .models import Booking, BookingService, Review, BookingPayment
from users.serializers import CustomerSerializer
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        read_only_fields = ['id', 'created_at']
        fields = '__all__'

class BookingServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingService
        read_only_fields = ['id', 'created_at']
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        read_only_fields = ['id', 'created_at']
        fields = '__all__'

class BookingPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingPayment
        read_only_fields = ['id', 'created_at']
        fields = '__all__'


class BookingCalendarSerializer(serializers.ModelSerializer):

    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 
            'status',
            'customer',
            'salon',
            'booking_services',
            'total_price',
            'selected_date',
            'booking_source'
        ]
        depth = 2

    def get_status(self, obj):
        return obj.get_status_display()

    def get_start_time(self, obj):
        return obj.start_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_end_time(self, obj):
        return obj.end_time.strftime('%Y-%m-%d %H:%M:%S')
    
    
        