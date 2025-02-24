from django.db import models
from salons.models import Service, Salon, Employee
from users.models import Customer
from datetime import timedelta

# Create your models here.


class Availability(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='availability')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_recurring = models.BooleanField(default=False)

    recurrence_choices = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    recurrence_pattern = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.employee.user.username} - {self.date} from {self.start_time} to {self.end_time}"
    


from django.db.models import Sum

class Booking(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
    ]

    BOOKING_SOURCE_CHOICES = [
        ('online', 'Online'),
        ('phone', 'Phone'),
        ('walk-in', 'Walk-in'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='booking_customer')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='booking_salon')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selected_date = models.DateField(null=True, blank=True)

    booking_source = models.CharField(max_length=20, choices=BOOKING_SOURCE_CHOICES, default='online')

    def calculate_total_price(self):
        """Calculate total price of all services in the booking"""
        total = self.booking_services.aggregate(
            total=Sum('price')
        )['total'] or 0
        self.total_price = total
        self.save()
        
    def __str__(self):
        return f"Booking #{self.id} - {self.customer.full_name} at {self.salon.name}"


class BookingService(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
    ]

    booking = models.ForeignKey(
        Booking, 
        on_delete=models.PROTECT, 
        related_name='booking_services',
        null=True, 
        blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.PROTECT, 
        related_name='booking_employee',
        null=True,
        blank=True
    )
    service = models.ForeignKey(
        Service, 
        on_delete=models.PROTECT, 
        related_name='booking_service',
        null=True,
        blank=True
    )
    duration = models.IntegerField(null=True, blank=True)
    is_requested = models.BooleanField(default=False)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.service.price

        if not self.start_at:
            self.start_at = self.booking.selected_date
        if not self.end_at:
            self.end_at = self.start_at + timedelta(minutes=self.duration)

        if not self.duration:
            self.duration = self.service.duration

        super().save(*args, **kwargs)
        self.booking.calculate_total_price()

    def __str__(self):
        return f"{self.service.name} - {self.employee.nick_name}"
    
    
    class Meta:
        verbose_name = 'Booking Service'
        verbose_name_plural = 'Booking Services'
        ordering = ['start_at']
    
    
class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT, related_name='reviews')
    salon = models.ForeignKey(Salon, on_delete=models.PROTECT, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.booking.user.email} at {self.salon.name}"
    

class BookingPayment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT, related_name='booking_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment for {self.booking.user.email} at {self.salon.name}"
    
    