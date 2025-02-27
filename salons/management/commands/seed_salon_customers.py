from django.core.management.base import BaseCommand
from salons.serializers import SalonCustomerSerializer

class Command(BaseCommand):
    help = 'Seeds 3 sample employees'

    def handle(self, *args, **kwargs):
        
        # Sample employee data with SalonCustomer
        salon_customers = [
            {
                'phone_number': '100123456',
                'full_name': 'John Doe',
                'address': '123 Main St, Anytown, USA',
                'email': 'john.doe@example.com',
                'birth_date': '1990-01-01',
                'gender': 'male',
                'salon': 1,
                'user': None,
            },
            {
                'phone_number': '100123457',
                'full_name': 'Jane Smith',
                'address': '456 Oak Ave, Anycity, USA',
                'email': 'jane.smith@example.com',
                'birth_date': '1985-02-14',
                'gender': 'female',
                'salon': 1,
            },
            {
                'phone_number': '100123458',
                'full_name': 'Bob Johnson',
                'address': '789 Pine Rd, Anyvillage, USA',
                'email': 'bob.johnson@example.com',
                'birth_date': '1980-03-20',
                'gender': 'other',
                'salon': 1,
            },
        ]

        for salon_customer in salon_customers:
            try:
                salon_customer = SalonCustomerSerializer(data=salon_customer)
                salon_customer.is_valid(raise_exception=True)
                salon_customer.save()
                self.stdout.write(self.style.SUCCESS(f'Created salon customer: {salon_customer["full_name"]}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating salon customer: {e}'))

      