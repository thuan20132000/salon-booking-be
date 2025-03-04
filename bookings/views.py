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
    SalonAppointmentsSerializer
)
from rest_framework import status
from django_filters import rest_framework as filters
# Create your views here.

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