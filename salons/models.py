from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Salon(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    opening_hours = models.TimeField(null=True, blank=True)
    closing_hours = models.TimeField(null=True, blank=True)
    business_hours = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    ROLES_CHOICES = [
        ('manager', 'Manager'),
        ('technician', 'Technician'),
        ('receptionist', 'Receptionist'),
        ('owner', 'Owner'),
    ]
    user = models.OneToOneField('auth.User', on_delete=models.PROTECT, related_name='employee')
    salon = models.ForeignKey(Salon, on_delete=models.PROTECT, related_name='employees', null=True, blank=True)
    role = models.CharField(max_length=255, choices=ROLES_CHOICES)
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nick_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.nick_name}"
    
    def save(self, *args, **kwargs):
        try:
            if self.user is None:  # Only create user if this is a new employee without a user
                self.user = User.objects.create_user(
                    username=self.phone_number, 
                    password=self.phone_number
                )
            super().save(*args, **kwargs)

        except Exception as e:
            print(e)    


class ServiceCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Service(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.PROTECT, related_name='services')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    is_active = models.BooleanField(default=True)
    deduction_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name='services', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} at {self.salon.name}"

