from django.db import models
from salons.models import Service, Salon, Employee
from users.models import Customer
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
        return f"{self.technician.user.username} - {self.date} from {self.start_time} to {self.end_time}"
    


from django.db.models import Sum

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_bookings')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='salon_bookings')
    booking_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def calculate_total_price(self):
        """Calculate total price of all services in the booking"""
        total = self.booking_services.aggregate(
            total=Sum('price')
        )['total'] or 0
        self.total_price = total
        self.save()
        
    def __str__(self):
        return f"Booking #{self.id} - {self.user.email} at {self.salon.name}"


class BookingService(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.PROTECT, related_name='booking_services')
    service_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.service.price
        super().save(*args, **kwargs)
        self.booking.calculate_total_price()

    def __str__(self):
        return f"{self.service.name} - {self.technician.user.username} - {self.booking.user.email}"
    
    
    class Meta:
        verbose_name = 'Booking Service'
        verbose_name_plural = 'Booking Services'
        ordering = ['service_time']
        unique_together = ['booking']
    
    
class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT, related_name='reviews')
    salon = models.ForeignKey(Salon, on_delete=models.PROTECT, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.booking.user.email} at {self.salon.name}"
    
    