from django.core.management.base import BaseCommand
from salons.models import Salon
from bookings.serializers import BookingSerializer, BookingServiceSerializer

class Command(BaseCommand):
    help = 'Seeds 3 sample bookings for salon_id 1'
    
    def handle(self, *args, **kwargs):  
        # Sample booking data
        bookings = [
            {
                'customer': 1,
                'status': 'scheduled',
                'selected_date': '2025-02-25',
                'total_price': 100.00,
                'notes': 'This is a test booking',
                'services': [
                    {
                        'service_id': 1,
                        'employee_id': 1,
                        'status': 'scheduled',
                        'start_at': '2025-02-25T10:00:00Z',
                        'end_at': '2025-02-25T11:00:00Z',
                        

                    }
                ]
            },
            {
                'customer': 2,
                'status': 'scheduled',
                'selected_date': '2025-02-25',
                'total_price': 150.00,
                'notes': 'This is a test booking',
                'services': [
                    {
                        'service_id': 2,
                        'employee_id': 2,
                        'status': 'scheduled',
                        'start_at': '2025-02-25T10:00:00Z',
                        'end_at': '2025-02-25T11:00:00Z',
                        
                    }
                ]
            },
            {
                'customer': 3,
                'status': 'scheduled',
                'selected_date': '2025-02-25',
                'total_price': 200.00,
                'notes': 'This is a test booking',
                'services': [
                    {
                        'service_id': 3,
                        'employee_id': 3,
                        'status': 'scheduled',
                        'start_at': '2025-02-25T10:00:00Z',
                        'end_at': '2025-02-25T11:00:00Z',

                    }
                ]
            },
        ]
        # add transaction

        for booking in bookings:
            booking['salon'] = 1
            booking_service_data = booking['services']
            booking = BookingSerializer(data=booking)
            booking.is_valid(raise_exception=True)
            try:
                booking_instance = booking.save()
                self.stdout.write(self.style.SUCCESS(f'Created booking: {booking_instance}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating booking: {e}'))

            for service in booking_service_data:
                booking_instance.booking_services.create(**service)
                try:
                    self.stdout.write(self.style.SUCCESS(f'Created service: {service}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating service: {e}'))

            self.stdout.write(self.style.SUCCESS(f'Created booking: {booking_instance}'))
