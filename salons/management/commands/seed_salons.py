from django.core.management.base import BaseCommand
from salons.models import Salon

class Command(BaseCommand):
    help = 'Seeds 3 sample salons'

    def handle(self, *args, **kwargs):
        # Sample salon data
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

        for salon_data in salons:
            salon = Salon.objects.create(**salon_data)
            self.stdout.write(self.style.SUCCESS(f'Created salon: {salon.name}'))
