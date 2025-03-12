from django.core.management.base import BaseCommand
from users.models import UserRole
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Seeds initial user roles and profiles'

    def handle(self, *args, **kwargs):
        # Create default roles
        roles = [
            'Admin',
            'Customer',
            'Technician',
            'Salon Owner',
        ]
        
        for role_name in roles:
            UserRole.objects.get_or_create(role=role_name)
            self.stdout.write(self.style.SUCCESS(f'Created role: {role_name}'))

        # Create a superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            superuser = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            
            # Get admin role
            admin_role = UserRole.objects.get(name='Admin')
            
            
            
            self.stdout.write(self.style.SUCCESS('Created superuser with profile'))

        self.stdout.write(self.style.SUCCESS('Seeding completed successfully'))
