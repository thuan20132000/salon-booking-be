from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Booking, BookingService
from .serializers import (
    BookingSerializer,
    BookingServiceSerializer, 
    BookingCalendarSerializer,
    BookingCreateSerializer,
    BookingUpdateSerializer,
    SalonAppointmentsSerializer,
    EmployeeServiceAppointmentSerializer,
    EmployeeBookingAvailabilitySerializer,
)
from rest_framework import status
from django_filters import rest_framework as filters
# Create your views here.

from datetime import datetime, timedelta
from django.utils import timezone

# create abstract viewset for booking and booking service
class BaseBookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def error_response(self, message):
        return Response({
            'message': message,
            'status_code': status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)

    def success_response(self, message, data=None, metadata=None, status_code=status.HTTP_200_OK):
        return Response({
            'message': message,
            'data': data,
            'metadata': metadata,
            'status_code': status_code
        }, status=status_code)

class BookingFilter(filters.FilterSet):
    salon_id = filters.NumberFilter(field_name='salon_id', lookup_expr='exact', required=True)
    selected_date = filters.DateFilter(field_name='selected_date', lookup_expr='exact', required=True)
    class Meta:
        model = Booking
        fields = ['salon_id', 'selected_date']

class BookingViewSet(BaseBookingViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def list(self, request):
        try:
            salon_id = request.query_params.get('salon_id')
            if not salon_id:
                return self.error_response('salon_id is required')
        
            bookings = Booking.objects.filter(salon_id=salon_id)
            serializer = BookingSerializer(bookings, many=True)
            return self.success_response('Bookings fetched successfully', serializer.data)
        except Exception as e:
            return self.error_response(str(e))


    def create(self, request):
        try:
            serializer = BookingCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return self.success_response('Booking created successfully', serializer.data)
            return self.error_response(serializer.errors)
        except Exception as e:
            return self.error_response(str(e))
        
    def retrieve(self, request, pk=None):
        try:
            booking = Booking.objects.get(pk=pk)
            serializer = self.serializer_class(booking)
            return self.success_response('Booking fetched successfully', serializer.data)
        except Booking.DoesNotExist:
            return self.error_response('Booking not found')

    def update(self, request, pk=None):
        try:    
            booking = Booking.objects.get(pk=pk)
            serializer = BookingUpdateSerializer(booking, data=request.data, partial=True)
            
            
            if serializer.is_valid():
                serializer.update_booking(booking, request.data)
                serializer.update_booking_services(booking, request.data)
                return self.success_response('Booking updated successfully', serializer.data)
            return self.error_response(serializer.errors)
        except Booking.DoesNotExist:
            return self.error_response('Booking not found')


    def destroy(self, request, pk=None):
        try:
            booking = Booking.objects.get(pk=pk)
            booking.delete()
            return self.success_response('Booking deleted successfully')
        except Booking.DoesNotExist:
            return self.error_response('Booking not found')
        
    @action(detail=True, methods=['patch'], url_path='update-booking-metadata')
    def update_booking_metadata(self, request, pk=None):
        try:
            booking = self.get_object()
            serializer = BookingUpdateSerializer(booking, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.update(booking, request.data)
                return self.success_response('Booking status updated successfully', serializer.data)
            return self.error_response(serializer.errors)
        except Booking.DoesNotExist:
            return self.error_response('Booking not found')

class BookingServiceViewSet(viewsets.ModelViewSet):
    queryset = BookingService.objects.all()
    serializer_class = BookingServiceSerializer

    http_method_names = ['get', 'post', 'put',  'patch', 'delete']



class BookingCalendarViewSet(BaseBookingViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingCalendarSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = BookingFilter

    def list(self, request):
        try:
            bookings = self.filter_queryset(self.get_queryset())
            serializer = BookingCalendarSerializer(bookings, many=True)
            metadata = {
                'total_bookings': bookings.count(),
            }
            return self.success_response('Bookings fetched successfully', serializer.data, metadata)
        except Exception as e:
            return self.error_response(str(e))

class SalonAppointmentsFilter(filters.FilterSet):

    salon_id = filters.NumberFilter(field_name='salon_id', lookup_expr='exact', required=True)
    selected_date = filters.DateFilter(field_name='selected_date', lookup_expr='exact', required=False)
    status = filters.ChoiceFilter(field_name='status', choices=Booking.STATUS_CHOICES, required=False)
    booking_source = filters.ChoiceFilter(field_name='booking_source', choices=Booking.BOOKING_SOURCE_CHOICES, required=False)
    
    class Meta:
        model = Booking
        fields = ['salon_id', 'selected_date', 'status']

class BookingAppointmentsViewSet(BaseBookingViewSet):
    queryset = Booking.objects.all()
    serializer_class = SalonAppointmentsSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = SalonAppointmentsFilter
    http_method_names = ['get']

    def list(self, request):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            metadata = {
                'total_bookings': queryset.count(),
            }
            return self.success_response('Bookings fetched successfully', serializer.data, metadata)
        except Exception as e:
            return self.error_response(str(e))

class EmployeeServiceAppointmentFilter(filters.FilterSet):
    employee_id = filters.NumberFilter(field_name='employee_id', lookup_expr='exact', required=True)
    booking__selected_date = filters.DateFilter(field_name='booking__selected_date', lookup_expr='exact', required=True)
    booking__status = filters.ChoiceFilter(field_name='booking__status', choices=BookingService.STATUS_CHOICES, required=False)
    class Meta:
        model = BookingService
        fields = [
            'employee_id',
            'status',
            'booking__selected_date',
            'booking__salon_id',
            'booking__status'
        ]

class EmployeeServiceAppointmentViewSet(BaseBookingViewSet):
    queryset = BookingService.objects.all()
    serializer_class = EmployeeServiceAppointmentSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EmployeeServiceAppointmentFilter
    http_method_names = ['get']

    def list(self, request):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            metadata = {
                'total_bookings': queryset.count(),
            }
            return self.success_response('Bookings fetched successfully', serializer.data, metadata)
        except Exception as e:
            return self.error_response(str(e))
        

class EmployeeBookingAvailabilityFilter(filters.FilterSet):
    employee_id = filters.NumberFilter(field_name='employee_id', lookup_expr='exact', required=True)
    booking__selected_date = filters.DateFilter(field_name='booking__selected_date', lookup_expr='exact', required=True)

    class Meta:
        model = BookingService
        fields = ['employee_id', 'booking__selected_date']


class EmployeeBookingAvailabilityViewSet(BaseBookingViewSet):
    queryset = BookingService.objects.all()
    serializer_class = EmployeeBookingAvailabilitySerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EmployeeBookingAvailabilityFilter

    def _generate_time_slots(
        self, 
        start_time, 
        next_booking_start_time, 
        service_duration, 
        interval_minutes=15
    ):
        """Helper function to generate time slots with specified interval"""
        slots = []
        current = start_time
        
        while current + timedelta(minutes=service_duration) <= next_booking_start_time:
            service_end = current + timedelta(minutes=service_duration)
            slots.append({
                'start': current.isoformat(),
                'end': service_end.isoformat(),
                'duration': service_duration
            })
            current += timedelta(minutes=interval_minutes)
        return slots

    
    def get_employee_booking_availability(self, request, *args, **kwargs):
        try:
            # Get date from query params
            selected_date = request.query_params.get('booking__selected_date')
            service_duration = request.query_params.get('service_duration')
            service_duration = int(service_duration) if service_duration else 15

            if not service_duration:
                return self.error_response('service_duration is required')

            if not selected_date:
                return self.error_response('selected_date is required')

            # Get filtered queryset based on existing filters (employee_id, date)
            queryset = self.filter_queryset(self.get_queryset())
            
            # Sort bookings by start time
            booked_slots = queryset.order_by('start_at')
            
            # Convert selected_date to datetime objects for start and end of day
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            start_of_day = timezone.make_aware(date_obj.replace(hour=9, minute=30))  # Assuming 9:3 AM opening
            end_of_day = timezone.make_aware(date_obj.replace(hour=19, minute=30))   # Assuming 5 PM closing
           
            # Generate available time slots between bookings
            available_slots = []
            current_time = start_of_day

            for booked_slot in booked_slots:
                # Calculate the latest possible start time that wouldn't overlap with the booking
                service_duration_time = timedelta(minutes=service_duration)
                latest_start = booked_slot.start_at - service_duration_time

                # If there's enough time before the booking, generate slots
                if current_time <= latest_start:
                    slots = self._generate_time_slots(
                        current_time,
                        next_booking_start_time=booked_slot.start_at,
                        service_duration=service_duration,
                        interval_minutes=10
                    )
                    available_slots.extend(slots)
                # Move current time to after this booking
                current_time = booked_slot.end_at

            # Add slots after the last booking until end of day
            if current_time < end_of_day:
                slots = self._generate_time_slots(
                    current_time,
                    end_of_day,
                    service_duration,
                    interval_minutes=10
                )
                available_slots.extend(slots)


            metadata = {
                'total_bookings': booked_slots.count(),
                'total_available_slots': len(available_slots),
                'service_duration': service_duration,
            }

            
            return self.success_response(
                'Employee booking availability fetched successfully',
                data=available_slots,
                metadata=metadata
            )
        except Exception as e:
            return self.error_response(str(e))
    
    @action(
            detail=False, 
            methods=['get'], 
            url_path='availability'
        )
    def get_availability(self, request, *args, **kwargs):
        print("get_availability")
        return self.get_employee_booking_availability(request, *args, **kwargs)