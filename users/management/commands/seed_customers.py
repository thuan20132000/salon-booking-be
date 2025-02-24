from django.core.management.base import BaseCommand
from users.models import Customer

class Command(BaseCommand):
    help = 'Seeds initial 5 customers  with random email and phone number'

    def handle(self, *args, **kwargs):
        customers = [
            {
                'full_name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone_number': '000222333',
            },
            {
                'full_name': 'Jane Smith',
                'email': 'jane.smith@example.com',
                'phone_number': '000222444',
            },
            {
                'full_name': 'Alice Johnson',
                'email': 'alice.johnson@example.com',
                'phone_number': '000222555',
            },
            {
                'full_name': 'Bob Brown',
                'email': 'bob.brown@example.com',
                'phone_number': '000222666',
            },
            {
                'full_name': 'Charlie Davis',
                'email': 'charlie.davis@example.com',
                'phone_number': '000222777',
            },
        ]

        for customer in customers:
             try:
                customer = Customer.objects.create(full_name=customer['full_name'], phone_number=customer['phone_number'])
                customer.save()
                self.stdout.write(self.style.SUCCESS(f'Created customer: {customer.full_name}'))
             except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating customer: {e}'))