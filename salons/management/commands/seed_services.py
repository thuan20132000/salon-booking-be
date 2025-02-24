from django.core.management.base import BaseCommand
from salons.models import Salon, Employee, Service
from salons.serializers import EmployeeSerializer

class Command(BaseCommand):
    help = 'Seeds sample services'

    def handle(self, *args, **kwargs):
        

        salons = [
            {
                'name': 'Glamour & Style',
                'description': 'A luxury salon offering premium beauty services',
                'address': '123 Main Street, New York, NY 10001',
                'phone': '212-555-0101',
                'email': 'glamour@example.com',
            },
            {
                'name': 'Chic Cuts',
                'description': 'Modern haircuts and styling for everyone',
                'address': '456 Fashion Ave, New York, NY 10002',
                'phone': '212-555-0102',
                'email': 'chiccuts@example.com',
            },
            {
                'name': 'Beauty Haven',
                'description': 'Your one-stop destination for all beauty needs',
                'address': '789 Beauty Blvd, New York, NY 10003',
                'phone': '212-555-0103',
                'email': 'beautyhaven@example.com',
            },
        ]


        # Sample services data
        services = [
            {
                'name': 'Pedicure',
                'duration': 40,
                'price': '39',
                'description': 'Includes a complimentary bath bomb, regular polish, nail shaping, cuticle trimming, foot scrub, massage and a hot towel.',
            },
            {
                'name': 'Pedicure With Shellac',
                'duration': 45,
                'price': '50',
                'description': 'Includes a complimentary bath bomb, shellac polish, nail shaping, cuticle trimming, foot scrub, massage and a hot towel.',
            },
            {
                'name': 'Manicure',
                'duration': 25,
                'price': '25',
                'description': 'Includes regular polish, nail shaping, cuticle trimming, lotion and a hot towel. Please select shellac removal if needed',
            },
            # Add more services as needed
        ]

        # Create services for each salon
        for salon in salons:
            for service in services:
                Service.objects.create(
                    name=service['name'],
                    duration=service['duration'],
                    price=service['price'],
                    description=service['description'],
                    salon=Salon.objects.get(name=salon['name'])
                )
                self.stdout.write(self.style.SUCCESS(f'Created service: {service["name"]}'))

        

        