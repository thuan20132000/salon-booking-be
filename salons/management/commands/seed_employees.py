from django.core.management.base import BaseCommand
from salons.models import Salon, Employee
from salons.serializers import EmployeeSerializer
class Command(BaseCommand):
    help = 'Seeds 3 sample employees'

    def handle(self, *args, **kwargs):
        
        # Sample employee data
        employees = [
            {
                'phone_number': '000123456',
                'role': 'manager',
                'nick_name': 'John',
            },
            {
                'phone_number': '000123457',
                'role': 'receptionist',
                'nick_name': 'Jane',
            },
            {
                'phone_number': '000123458',
                'role': 'technician',
                'nick_name': 'Bob',
            },
        ]

        for employee in employees:
            try:
                employee = EmployeeSerializer(data=employee)
                employee.is_valid(raise_exception=True)
                employee.save()
                self.stdout.write(self.style.SUCCESS(f'Created employee: {employee["nick_name"]}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating employee: {e}'))

      