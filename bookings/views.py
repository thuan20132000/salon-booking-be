from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Booking, BookingService
from .serializers import (
    BookingSerializer,
    BookingServiceSerializer, 
    BookingCalendarSerializer,
    BookingCreateSerializer,
    BookingUpdateSerializer
)
from rest_framework import status
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

    def success_response(self, message, data=None):
        return Response({
            'message': message,
            'data': data,
            'status_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

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
                serializer.update(booking, request.data)
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

class BookingServiceViewSet(viewsets.ModelViewSet):
    queryset = BookingService.objects.all()
    serializer_class = BookingServiceSerializer

    http_method_names = ['get', 'post', 'put',  'patch', 'delete']



class BookingCalendarViewSet(BaseBookingViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingCalendarSerializer
    

    def list(self, request):
        salon_id = request.query_params.get('salon_id')
        if not salon_id:
            return self.error_response('salon_id is required')
        
        bookings = Booking.objects.filter(salon_id=salon_id)
        serializer = BookingCalendarSerializer(bookings, many=True)

        return self.success_response('Bookings fetched successfully', serializer.data)
