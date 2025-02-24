from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Booking, BookingService
from .serializers import (
    BookingSerializer,
    BookingServiceSerializer, 
    BookingCalendarSerializer 
)
from rest_framework import status
# Create your views here.

# create abstract viewset for booking and booking service
class BaseBookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def error_response(self, message):
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

class BookingViewSet(BaseBookingViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @action(
        detail=False, 
        methods=['get'],
        url_path='booking-calendar'
    )
    def booking_calendar(self, request):
        salon_id = request.query_params.get('salon_id')
        if not salon_id:
            return self.error_response('salon_id is required')
        
        salon_bookings = Booking.objects.filter(salon_id=salon_id)
        serializer = BookingCalendarSerializer(salon_bookings, many=True)
        return Response(serializer.data)

class BookingServiceViewSet(viewsets.ModelViewSet):
    queryset = BookingService.objects.all()
    serializer_class = BookingServiceSerializer

