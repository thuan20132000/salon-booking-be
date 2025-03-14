from rest_framework import serializers
from .models import Booking, BookingService, Review, BookingPayment
from salons.serializers import SalonCustomerSerializer, EmployeeSerializer
from salons.models import SalonCustomer

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        read_only_fields = ['id', 'created_at']
        fields = '__all__'

class BookingCreateSerializer(serializers.ModelSerializer):
    services = serializers.ListField(write_only=True, required=True)

    class Meta:
        model = Booking
        read_only_fields = ['id', 'created_at']
        fields = '__all__'

    def create(self, validated_data):
        services = validated_data.pop('services', [])

        booking_services = self.initial_data.get('services', [])
        booking = Booking.objects.create(**validated_data)

        for service in booking_services:
            BookingService.objects.create(booking=booking, **service)

        print("created booking:: ", booking)
        
        return booking

    def to_representation(self, instance):
        return BookingCalendarSerializer(instance).data

class BookingUpdateSerializer(serializers.ModelSerializer):
    services = serializers.ListField(write_only=True, required=True)

    class Meta:
        model = Booking
        read_only_fields = ['id', 'created_at']
        fields = '__all__'

    def update_booking(self, instance, validated_data):
        self.update(instance=instance, validated_data=validated_data)
        return instance

    def update_booking_services(self, instance, validated_data):

        
        # update instance fields
        booking_services = self.initial_data.get('services', [])

        # remove all existing services
        BookingService.objects.filter(booking=instance).delete()

        # create new services   
        for service in booking_services:
            BookingService.objects.create(booking=instance, **service)

    
    def to_representation(self, instance):
        return BookingCalendarSerializer(instance).data
    

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

    customer = SalonCustomerSerializer(read_only=True)

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
            'booking_source',
        ]
        depth = 2

    def get_status(self, obj):
        return obj.get_status_display()

    def get_start_time(self, obj):
        return obj.start_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_end_time(self, obj):
        return obj.end_time.strftime('%Y-%m-%d %H:%M:%S')
    
    

class SalonAppointmentsSerializer(serializers.ModelSerializer):
    customer = SalonCustomerSerializer(read_only=True)
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


class EmployeeServiceAppointmentSerializer(serializers.ModelSerializer):

    employee = EmployeeSerializer(read_only=True)
    class Meta:
        model = BookingService
        fields = '__all__'
        depth = 2

    def get_status(self, obj):
        return obj.get_status_display()
    
    def get_booking_source(self, obj):
        return obj.get_booking_source_display()


class EmployeeBookingAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingService
        fields = '__all__'
        depth = 2


class CustomerBookingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        depth = 2

